"""
Phase 2-3: Website research + AI company analysis + lead scoring.

For every lead in status NEW (or research_status PENDING):
  1. fetch a few relevant pages from the website (best-effort, never blocks the pipeline)
  2. ask the AI model for structured JSON analysis
  3. compute a 0-100 lead score
  4. save everything, move status -> RESEARCHED

Usage:
    python scripts/ai_analysis.py [--limit N]
"""
import argparse
import json
import sys

from ai_client import chat_json
from config import AI_MODEL
from db import get_connection, log_event, now_iso
from fetch_website import research_website
from scoring import compute_lead_score, priority_band

PROMPT_PATH = "../prompts/company_research_prompt.txt"

REQUIRED_KEYS = [
    "company_summary", "business_type", "services", "observed_features",
    "possible_manual_processes", "pain_points", "automation_opportunities",
    "recommended_weboost_solution", "reasoning_summary", "personalization_fact",
    "is_freight_broker", "broker_evidence", "owner_name", "owner_title", "company_scale", "confidence",
]


GENERIC_MAILBOXES = {
    "info", "contact", "sales", "dispatch", "office", "admin", "support", "hello", "ops", "operations", "team",
    "booking", "quotes", "quote", "mail", "brokerage", "carriers", "carrier", "accounting", "billing", "logistics",
}


def name_fits_mailbox(full_name: str, email: str) -> bool:
    """Greet by name only if the mailbox is generic or is clearly this person's own address.
    Avoids "Hi Daniel" landing in vsmith@'s inbox."""
    local = email.split("@")[0].lower()
    if local in GENERIC_MAILBOXES:
        return True
    names = [p.lower().strip(".,") for p in full_name.split() if len(p.strip(".,")) > 2]
    return any(n in local for n in names)


def load_prompt_template() -> str:
    with open(PROMPT_PATH, "r", encoding="utf-8") as f:
        return f.read()


def call_ai_analysis(template: str, lead: dict, website_text: str) -> dict:
    prompt = template
    for key, value in {
        "{company_name}": lead["company_name"] or "",
        "{industry}": lead["industry"] or "",
        "{city}": lead["city"] or "",
        "{state}": lead["state"] or "",
        "{website}": lead["website"] or "",
        "{website_text}": website_text or "(no website text available)",
    }.items():
        prompt = prompt.replace(key, value)

    data = chat_json(prompt, "analysis")

    for key in REQUIRED_KEYS:
        data.setdefault(key, [] if key in ("services", "observed_features", "possible_manual_processes",
                                            "pain_points", "automation_opportunities") else "")
    return data


def process_lead(template: str, conn, lead: dict) -> None:
    lead_id = lead["id"]

    research = research_website(lead["website"])
    conn.execute(
        "UPDATE leads SET research_status = ?, updated_at = ? WHERE id = ?",
        (research["status"], now_iso(), lead_id),
    )
    conn.commit()
    log_event(
        conn, lead_id, "WEBSITE_FETCHED",
        "OK" if research["status"] != "FAILED" else "ERROR",
        research["error"] or f"{len(research['pages_fetched'])} page(s) fetched",
    )

    try:
        analysis = call_ai_analysis(template, lead, research["text"])
    except Exception as e:
        conn.execute(
            "UPDATE leads SET status = 'ERROR', updated_at = ? WHERE id = ?",
            (now_iso(), lead_id),
        )
        conn.commit()
        log_event(conn, lead_id, "AI_ANALYSIS_COMPLETED", "ERROR", str(e))
        print(f"  [ERROR] {lead['company_name']}: {e}")
        return

    score, reasons = compute_lead_score(lead, analysis)

    # ICP gate: only confirmed freight brokers go on to email generation
    if research["status"] == "FAILED":
        next_status = "SKIPPED_NO_SITE"
    elif not analysis.get("is_freight_broker"):
        next_status = "NOT_ICP"
    elif str(analysis.get("company_scale", "")).lower() == "large":
        next_status = "TOO_LARGE"
    else:
        next_status = "RESEARCHED"

    conn.execute(
        """
        UPDATE leads SET
            website_summary = ?, business_type = ?, observed_features = ?,
            pain_points = ?, automation_opportunities = ?, recommended_solution = ?,
            ai_analysis_json = ?, lead_score = ?, score_reasons = ?,
            status = ?, updated_at = ?
        WHERE id = ?
        """,
        (
            analysis["company_summary"],
            analysis["business_type"],
            json.dumps(analysis["observed_features"]),
            json.dumps(analysis["pain_points"]),
            json.dumps(analysis["automation_opportunities"]),
            analysis["recommended_weboost_solution"],
            json.dumps(analysis),
            score,
            json.dumps(reasons),
            next_status,
            now_iso(),
            lead_id,
        ),
    )
    owner = (analysis.get("owner_name") or "").strip()
    if owner and not (lead.get("contact_first_name") or "").strip():
        parts = owner.split()
        greet = parts[0] if name_fits_mailbox(owner, lead.get("contact_email") or "") else ""
        conn.execute(
            """UPDATE leads SET contact_full_name = ?, contact_first_name = ?, contact_last_name = ?,
               contact_role = ? WHERE id = ?""",
            (owner, greet, parts[-1] if len(parts) > 1 else "", analysis.get("owner_title") or "", lead_id),
        )
    conn.commit()
    log_event(conn, lead_id, "AI_ANALYSIS_COMPLETED", "OK", f"score={score} -> {next_status}")

    print(f"  {lead['company_name']:<30} score={score:>3} ({priority_band(score)})  research={research['status']}  -> {next_status}")


def main(limit: int) -> None:
    template = load_prompt_template()

    conn = get_connection()
    leads = conn.execute(
        "SELECT * FROM leads WHERE status = 'NEW' ORDER BY created_at LIMIT ?", (limit,)
    ).fetchall()

    if not leads:
        print("No leads with status NEW to process.")
        return

    print(f"Analyzing {len(leads)} lead(s) with model {AI_MODEL}...\n")
    for row in leads:
        process_lead(template, conn, dict(row))

    conn.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=50)
    args = parser.parse_args()
    main(args.limit)
