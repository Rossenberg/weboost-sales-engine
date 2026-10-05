"""
Two-way sync with the Cloudflare dashboard.

1. PULL: approvals / rejections / edits / "do not contact" / meetings made in the dashboard are applied
   to the local database; AI-training rules are written to prompts/style_rules.txt.
2. PUSH: a full snapshot of leads + messages + events + AI usage + settings goes to the dashboard.

Usage:
    python scripts/sync_dashboard.py
Needs DASHBOARD_URL and DASHBOARD_SYNC_TOKEN in .env.
"""
import json
import os
from pathlib import Path

os.chdir(Path(__file__).resolve().parent)

import requests

from config import (
    AUTO_SEND, DAILY_SEND_LIMIT, DASHBOARD_SYNC_TOKEN, DASHBOARD_URL, DRY_RUN, ROOT, SEND_START_DATE, STYLE_RULES_PATH,
)
from db import get_connection, log_event, now_iso
from send_queue import daily_cap

POOL_CSV = ROOT / "data" / "fmcsa_brokers.csv"


def call(method: str, path: str, payload=None):
    if not DASHBOARD_URL or not DASHBOARD_SYNC_TOKEN:
        raise SystemExit("DASHBOARD_URL / DASHBOARD_SYNC_TOKEN are not set in .env")
    r = requests.request(method, DASHBOARD_URL.rstrip("/") + path, json=payload, timeout=60,
                         headers={"Authorization": f"Bearer {DASHBOARD_SYNC_TOKEN}"})
    r.raise_for_status()
    return r.json()


def pull(conn) -> None:
    data = call("GET", "/api/sync/pull")
    applied = []
    for a in data.get("actions", []):
        lead_id, act, ts = a["lead_id"], a["action"], now_iso()
        if act == "approve":
            conn.execute("UPDATE leads SET status='APPROVED', updated_at=? WHERE id=? AND status IN ('READY','REJECTED')", (ts, lead_id))
        elif act == "edit_approve":
            conn.execute("UPDATE leads SET email_subject=?, email_body=?, status='APPROVED', updated_at=? WHERE id=? AND status IN ('READY','REJECTED','APPROVED')",
                         (a["subject"], a["body"], ts, lead_id))
        elif act == "reject":
            conn.execute("UPDATE leads SET status='REJECTED', updated_at=? WHERE id=? AND status IN ('READY','APPROVED')", (ts, lead_id))
        elif act == "reopen":
            conn.execute("UPDATE leads SET status='READY', updated_at=? WHERE id=? AND status='REJECTED'", (ts, lead_id))
        elif act == "meeting":
            conn.execute("UPDATE leads SET meeting_booked=1, status='MEETING_BOOKED', next_followup_at=NULL, updated_at=? WHERE id=?", (ts, lead_id))
        elif act == "dnc":
            conn.execute("UPDATE leads SET do_not_contact=1, next_followup_at=NULL, updated_at=? WHERE id=?", (ts, lead_id))
        conn.commit()
        log_event(conn, lead_id, f"DASHBOARD_{act.upper()}", "OK", a.get("note") or "")
        applied.append(a["id"])
    if applied:
        call("POST", "/api/sync/ack", {"ids": applied})

    rules = [r["text"].strip() for r in data.get("rules", []) if r["text"].strip()]
    STYLE_RULES_PATH.write_text("\n".join(f"- {r}" for r in rules) + ("\n" if rules else ""), encoding="utf-8")
    print(f"pull: {len(applied)} action(s) applied, {len(rules)} AI rule(s)")


def lead_row(r) -> dict:
    a = json.loads(r["ai_analysis_json"] or "{}")
    return {
        "id": r["id"], "company_name": r["company_name"], "website": r["website"], "state": r["state"], "city": r["city"],
        "contact_name": r["contact_full_name"], "contact_role": r["contact_role"], "contact_email": r["contact_email"],
        "phone": r["phone"], "mc_number": r["mc_number"], "status": r["status"], "research_status": r["research_status"],
        "lead_score": r["lead_score"], "business_type": r["business_type"], "personalization_fact": a.get("personalization_fact"),
        "broker_evidence": a.get("broker_evidence"), "company_scale": a.get("company_scale"), "summary": r["website_summary"],
        "email_subject": r["email_subject"], "email_body": r["email_body"],
        "initial_email_sent_at": r["initial_email_sent_at"], "followup_1_sent_at": r["followup_1_sent_at"],
        "followup_2_sent_at": r["followup_2_sent_at"], "followup_3_sent_at": r["followup_3_sent_at"],
        "next_followup_at": r["next_followup_at"], "last_contact_at": r["last_contact_at"],
        "reply_received": r["reply_received"], "reply_text": r["reply_text"], "reply_received_at": r["reply_received_at"],
        "reply_category": r["reply_category"], "reply_sentiment": r["reply_sentiment"], "lead_probability": r["lead_probability"],
        "reply_reasoning": r["reply_reasoning"], "next_action": r["next_action"], "do_not_contact": r["do_not_contact"],
        "meeting_booked": r["meeting_booked"], "created_at": r["created_at"], "updated_at": r["updated_at"],
    }


def push(conn) -> None:
    from datetime import date
    leads = [lead_row(r) for r in conn.execute("SELECT * FROM leads WHERE source != 'test_data'")]
    ids = {l["id"] for l in leads}
    messages = [dict(r) for r in conn.execute("SELECT id, lead_id, kind, subject, body, created_at FROM messages") if r["lead_id"] in ids]
    events = [dict(r) for r in conn.execute("SELECT id, lead_id, timestamp, action, status, detail FROM lead_events") if r["lead_id"] in ids]
    usage = [dict(r) for r in conn.execute("SELECT id, created_at, step, model, input_tokens, output_tokens, cost_usd FROM api_usage")]
    pool_total = sum(1 for _ in open(POOL_CSV, encoding="utf-8")) - 1 if POOL_CSV.exists() else 0
    meta = {
        "pool_total": pool_total,
        "pool_imported": conn.execute("SELECT COUNT(*) FROM leads WHERE source = 'fmcsa_broker_registry'").fetchone()[0],
        "dry_run": str(DRY_RUN or not AUTO_SEND).lower(),
        "daily_cap": daily_cap(date.today()) or 0,
        "daily_limit": DAILY_SEND_LIMIT,
        "send_start_date": SEND_START_DATE,
    }
    res = call("POST", "/api/sync/push", {"full_leads": True, "leads": leads, "messages": messages, "events": events, "usage": usage, "meta": meta})
    print(f"push: {res.get('leads')} lead(s), {len(messages)} message(s), {len(events)} event(s), {len(usage)} AI call(s)")


def main() -> None:
    conn = get_connection()
    pull(conn)
    push(conn)


if __name__ == "__main__":
    main()
