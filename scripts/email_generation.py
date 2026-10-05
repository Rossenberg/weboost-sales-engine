"""
Phase 4: Personalized email generation.

For every lead in status RESEARCHED (and score >= MIN_LEAD_SCORE):
  1. build a prompt from the AI analysis already stored on the lead
  2. ask the AI model for a subject + body (JSON)
  3. assemble the final email (greeting + body + signature)
  4. save it, move status -> READY (awaiting human approval, per review mode)

Usage:
    python scripts/email_generation.py [--limit N]
"""
import argparse
import json
import random

from ai_client import chat_json
from config import MIN_LEAD_SCORE, SENDER_NAME, BOOKING_URL, SENDER_BACKGROUND, STYLE_RULES_PATH
from db import get_connection, log_event, now_iso

PROMPT_PATH = "../prompts/email_generation_prompt.txt"

ENDING_STYLES = [
    "One short question asking whether sorting carrier replies eats time on their side. Do not offer a walkthrough.",
    "Offer to send a 60-second screen recording of how it works; ask if they want it. No other question.",
    "Ask how they handle carrier replies today, in one casual sentence.",
    "Say you are looking for two brokerages to test it with for free and ask if they'd be open to it.",
    "A soft close: 'No pitch intended, curious if this is even a problem for you.'",
]
SUBJECT_STYLES = [
    "a plain question about carrier replies",
    "two or three lowercase words, like a quick note from a colleague",
    "mention the load board / posting loads angle, no company name",
    "short statement of the idea, no question mark",
]


def load_prompt_template() -> str:
    with open(PROMPT_PATH, "r", encoding="utf-8") as f:
        return f.read()


def style_rules() -> str:
    """Rules the user wrote in the dashboard ("AI training"); empty if none yet."""
    try:
        text = STYLE_RULES_PATH.read_text(encoding="utf-8").strip()
    except FileNotFoundError:
        return ""
    return text


def build_prompt(template: str, lead: dict, analysis: dict) -> str:
    prompt = template
    replacements = {
        "{first_name}": lead["contact_first_name"] or "there",
        "{company_name}": lead["company_name"] or "",
        "{business_type}": analysis.get("business_type", ""),
        "{personalization_fact}": analysis.get("personalization_fact", ""),
        "{automation_opportunities}": "; ".join(analysis.get("automation_opportunities", [])),
        "{recommended_solution}": analysis.get("recommended_weboost_solution", ""),
        "{sender_background}": SENDER_BACKGROUND,
        "{ending_style}": random.choice(ENDING_STYLES),
        "{subject_style}": random.choice(SUBJECT_STYLES),
        "{booking_url}": BOOKING_URL or "(none provided - do not include a link)",
    }
    for key, value in replacements.items():
        prompt = prompt.replace(key, value)
    rules = style_rules()
    if rules:
        prompt += "\nEXTRA RULES FROM THE SENDER (follow them, they override the style above):\n" + rules + "\n"
    return prompt


def assemble_email(first_name: str, body: str) -> str:
    greeting = f"Hi {first_name}," if first_name and first_name != "there" else "Hi,"
    signature = f"\n\n— {SENDER_NAME}\nWeBoost\nweboost.live"
    return f"{greeting}\n\n{body.strip()}{signature}"


def process_lead(template: str, conn, lead: dict) -> None:
    lead_id = lead["id"]
    analysis = json.loads(lead["ai_analysis_json"] or "{}")

    prompt = build_prompt(template, lead, analysis)

    try:
        data = chat_json(prompt, "email")
    except Exception as e:
        log_event(conn, lead_id, "EMAIL_GENERATED", "ERROR", str(e))
        print(f"  [ERROR] {lead['company_name']}: {e}")
        return

    subject = data.get("subject", "").strip()
    body = assemble_email(lead["contact_first_name"], data.get("body", ""))

    conn.execute(
        """
        UPDATE leads SET email_subject = ?, email_body = ?, status = 'READY', updated_at = ?
        WHERE id = ?
        """,
        (subject, body, now_iso(), lead_id),
    )
    conn.commit()
    log_event(conn, lead_id, "EMAIL_GENERATED", "OK", subject)

    print(f"  {lead['company_name']:<30} -> subject: \"{subject}\"")


def main(limit: int) -> None:
    template = load_prompt_template()

    conn = get_connection()
    leads = conn.execute(
        "SELECT * FROM leads WHERE status = 'RESEARCHED' AND lead_score >= ? ORDER BY lead_score DESC LIMIT ?",
        (MIN_LEAD_SCORE, limit),
    ).fetchall()

    if not leads:
        print("No RESEARCHED leads above MIN_LEAD_SCORE to generate emails for.")
        return

    print(f"Generating emails for {len(leads)} lead(s)...\n")
    for row in leads:
        process_lead(template, conn, dict(row))

    conn.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=50)
    args = parser.parse_args()
    main(args.limit)
