"""
Send due follow-ups and approved first emails, respecting the daily ramp-up cap.

Order each run: follow-ups first (they keep live threads warm), then new APPROVED first emails.
- First emails: status APPROVED, do_not_contact = 0, has an email.
- Follow-ups: status SENT / FOLLOWUP_1 / FOLLOWUP_2, no reply, next_followup_at <= now.
  Sent as a reply in the same thread ("Re: <subject>", In-Reply-To = previous Message-ID).
  After follow-up 3 the lead moves to SEQUENCE_DONE.
DRY_RUN=true (default) prints what would be sent and changes nothing.

Usage:
    python scripts/send_queue.py [--limit N]
"""
import argparse
import random
import time
from datetime import date, datetime, timedelta, timezone

from ai_client import chat_json
from config import (
    AUTO_SEND, DRY_RUN, DAILY_SEND_LIMIT, FOLLOWUP_1_DAYS, FOLLOWUP_2_DAYS, FOLLOWUP_3_DAYS, GMAIL_USER,
    SEND_DELAY_SECONDS, SEND_RAMP, SEND_START_DATE, STYLE_RULES_PATH,
)
from db import get_connection, log_event, log_message, now_iso
from mailer import build_message, send

FOLLOWUP_PROMPT = "../prompts/followup_prompt.txt"
# status before the send -> (follow-up number, status after, days after the first email for the NEXT follow-up)
FOLLOWUP_STEPS = {
    "SENT": (1, "FOLLOWUP_1", FOLLOWUP_2_DAYS),
    "FOLLOWUP_1": (2, "FOLLOWUP_2", FOLLOWUP_3_DAYS),
    "FOLLOWUP_2": (3, "FOLLOWUP_3", None),
}


def daily_cap(today: date) -> int:
    if not SEND_START_DATE:
        return 0  # sending not started: warm-up phase
    days = (today - date.fromisoformat(SEND_START_DATE)).days
    if days < 0:
        return 0
    cap = 0
    for from_day, per_day in SEND_RAMP:
        if days >= from_day:
            cap = per_day
    return min(cap, DAILY_SEND_LIMIT)


def sent_today(conn) -> int:
    start = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0).isoformat()
    return conn.execute(
        "SELECT COUNT(*) FROM lead_events WHERE action IN ('EMAIL_SENT', 'FOLLOWUP_SENT') AND status = 'OK' AND timestamp >= ?",
        (start,),
    ).fetchone()[0]


def live() -> bool:
    return not DRY_RUN and AUTO_SEND


def followup_text(lead, number: int) -> str:
    try:
        rules = STYLE_RULES_PATH.read_text(encoding="utf-8").strip()
    except FileNotFoundError:
        rules = ""
    prompt = open(FOLLOWUP_PROMPT, encoding="utf-8").read()
    for k, v in {
        "{followup_number}": str(number),
        "{style_rules}": ("EXTRA RULES FROM THE SENDER:\n" + rules + "\n") if rules else "",
        "{first_subject}": lead["email_subject"] or "",
        "{first_body}": lead["email_body"] or "",
    }.items():
        prompt = prompt.replace(k, v)
    return chat_json(prompt, "followup")["body"].strip()


def send_followups(conn, budget: int) -> int:
    now = now_iso()
    due = conn.execute(
        """SELECT * FROM leads WHERE status IN ('SENT', 'FOLLOWUP_1', 'FOLLOWUP_2')
             AND reply_received = 0 AND do_not_contact = 0
             AND next_followup_at IS NOT NULL AND next_followup_at <= ?
           ORDER BY next_followup_at LIMIT ?""",
        (now, budget),
    ).fetchall()
    done = 0
    for lead in due:
        number, new_status, next_days = FOLLOWUP_STEPS[lead["status"]]
        label = f"{lead['company_name']} <{lead['contact_email']}>"
        if not live():
            print(f"[DRY RUN] would send follow-up {number} to {label}")
            continue
        try:
            body = followup_text(lead, number)
            subject = "Re: " + (lead["email_subject"] or "")
            msg = build_message(lead["contact_email"], subject, body, in_reply_to=lead["last_message_id"] or "")
            message_id = send(msg)
        except Exception as e:
            log_event(conn, lead["id"], "FOLLOWUP_SENT", "ERROR", str(e))
            print(f"[ERROR] follow-up {number} {label}: {e}")
            continue
        first = datetime.fromisoformat(lead["initial_email_sent_at"])
        next_fu = (first + timedelta(days=next_days)).isoformat() if next_days else None
        ts = now_iso()
        conn.execute(
            f"""UPDATE leads SET status = ?, followup_{number}_sent_at = ?, last_contact_at = ?,
                next_followup_at = ?, last_message_id = ?, updated_at = ? WHERE id = ?""",
            (new_status if next_days else "SEQUENCE_DONE", ts, ts, next_fu, message_id, ts, lead["id"]),
        )
        conn.commit()
        log_message(conn, lead["id"], f"followup_{number}", subject, body, message_id)
        log_event(conn, lead["id"], "FOLLOWUP_SENT", "OK", f"#{number} {message_id}")
        print(f"[FOLLOW-UP {number}] {label}")
        done += 1
        time.sleep(random.randint(*SEND_DELAY_SECONDS))
    return done


def send_first_emails(conn, budget: int) -> int:
    leads = conn.execute(
        """SELECT * FROM leads
           WHERE status = 'APPROVED' AND do_not_contact = 0
             AND contact_email IS NOT NULL AND contact_email != ''
           ORDER BY lead_score DESC LIMIT ?""",
        (budget,),
    ).fetchall()
    done = 0
    for i, lead in enumerate(leads):
        label = f"{lead['company_name']} <{lead['contact_email']}>"
        if not live():
            print(f"[DRY RUN] would send to {label}: \"{lead['email_subject']}\"")
            continue
        try:
            msg = build_message(lead["contact_email"], lead["email_subject"], lead["email_body"])
            message_id = send(msg)
        except Exception as e:
            log_event(conn, lead["id"], "EMAIL_SENT", "ERROR", str(e))
            print(f"[ERROR] {label}: {e}")
            continue
        ts = now_iso()
        next_fu = (datetime.now(timezone.utc) + timedelta(days=FOLLOWUP_1_DAYS)).isoformat()
        conn.execute(
            """UPDATE leads SET status = 'SENT', initial_email_sent_at = ?, last_contact_at = ?,
               next_followup_at = ?, last_message_id = ?, updated_at = ? WHERE id = ?""",
            (ts, ts, next_fu, message_id, ts, lead["id"]),
        )
        conn.commit()
        log_message(conn, lead["id"], "initial", lead["email_subject"], lead["email_body"], message_id)
        log_event(conn, lead["id"], "EMAIL_SENT", "OK", message_id)
        print(f"[SENT] {label}")
        done += 1
        if i < len(leads) - 1:
            time.sleep(random.randint(*SEND_DELAY_SECONDS))
    return done


def main(limit: int) -> None:
    conn = get_connection()
    cap = daily_cap(date.today())
    remaining = max(0, cap - sent_today(conn))
    print(f"mailbox {GMAIL_USER or '(not set)'} | daily cap {cap} | already sent today {cap - remaining} "
          f"| DRY_RUN={DRY_RUN} AUTO_SEND={AUTO_SEND}")
    if remaining == 0:
        print("Nothing to send today (cap reached or SEND_START_DATE not set/reached).")
        return
    budget = min(limit, remaining)
    used = send_followups(conn, budget)
    send_first_emails(conn, budget - used)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=50)
    main(ap.parse_args().limit)
