"""
Read the mailbox over IMAP and update leads: replies, bounces, unsubscribes.

- Matches an incoming message to a lead by sender address, or by In-Reply-To = last_message_id.
- Bounces (MAILER-DAEMON / delivery failure) -> BOUNCED, do_not_contact = 1.
- "unsubscribe" / "stop" / "remove me" -> UNSUBSCRIBED, do_not_contact = 1.
- Anything else -> REPLIED, text saved (AI classification is a later step).
Follow-ups are never sent to leads in these states.

Usage:
    python scripts/check_replies.py [--days 3]
"""
import argparse
import email
import imaplib
import re
from datetime import date, timedelta
from email.header import decode_header, make_header
from email.utils import parseaddr

from config import GMAIL_APP_PASSWORD, GMAIL_USER
from db import get_connection, log_event, log_message, now_iso

UNSUB_RE = re.compile(r"\b(unsubscribe|remove me|stop (emailing|sending|contacting)|do not (contact|email))\b", re.I)


def text_of(msg) -> str:
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain" and not part.get_filename():
                return part.get_payload(decode=True).decode(part.get_content_charset() or "utf-8", "replace")
        return ""
    payload = msg.get_payload(decode=True)
    return payload.decode(msg.get_content_charset() or "utf-8", "replace") if payload else ""


def first_reply_lines(body: str, n: int = 40) -> str:
    out = []
    for line in body.splitlines():
        if line.startswith(">") or re.match(r"On .+ wrote:", line):
            break
        out.append(line)
    return "\n".join(out[:n]).strip()


def main(days: int) -> None:
    if not GMAIL_USER or not GMAIL_APP_PASSWORD:
        raise SystemExit("GMAIL_USER / GMAIL_APP_PASSWORD are not set in .env")
    conn = get_connection()
    imap = imaplib.IMAP4_SSL("imap.gmail.com")
    imap.login(GMAIL_USER, GMAIL_APP_PASSWORD)
    imap.select("INBOX")
    since = (date.today() - timedelta(days=days)).strftime("%d-%b-%Y")
    _, data = imap.search(None, f'(SINCE "{since}")')
    ids = data[0].split()
    print(f"{len(ids)} message(s) since {since}")

    handled = 0
    for num in ids:
        _, raw = imap.fetch(num, "(RFC822)")
        msg = email.message_from_bytes(raw[0][1])
        sender = parseaddr(msg.get("From", ""))[1].lower()
        subject = str(make_header(decode_header(msg.get("Subject", ""))))
        body = text_of(msg)
        in_reply_to = (msg.get("In-Reply-To") or "").strip()
        incoming_id = (msg.get("Message-ID") or "").strip()
        if incoming_id and conn.execute("SELECT 1 FROM messages WHERE message_id = ?", (incoming_id,)).fetchone():
            continue  # already processed on an earlier run

        is_bounce = "mailer-daemon" in sender or "postmaster" in sender or "delivery status" in subject.lower()
        if is_bounce:
            m = re.search(r"[\w.+-]+@[\w-]+\.[\w.-]+", body)
            failed = m.group(0).lower() if m else ""
            lead = conn.execute("SELECT * FROM leads WHERE lower(contact_email) = ?", (failed,)).fetchone() if failed else None
            if lead and lead["status"] not in ("BOUNCED",):
                conn.execute("UPDATE leads SET status='BOUNCED', do_not_contact=1, updated_at=? WHERE id=?", (now_iso(), lead["id"]))
                conn.commit()
                log_event(conn, lead["id"], "BOUNCED", "OK", subject)
                handled += 1
                print(f"[BOUNCE] {lead['company_name']}")
            continue

        lead = conn.execute("SELECT * FROM leads WHERE lower(contact_email) = ?", (sender,)).fetchone()
        if not lead and in_reply_to:
            lead = conn.execute("SELECT * FROM leads WHERE last_message_id = ?", (in_reply_to,)).fetchone()
        if not lead or lead["reply_received"]:
            continue
        log_message(conn, lead["id"], "reply_in", subject, first_reply_lines(body, 200), incoming_id)

        text = first_reply_lines(body)
        if UNSUB_RE.search(text) or UNSUB_RE.search(subject):
            conn.execute(
                "UPDATE leads SET status='UNSUBSCRIBED', do_not_contact=1, reply_received=1, reply_text=?, reply_received_at=?, updated_at=? WHERE id=?",
                (text, now_iso(), now_iso(), lead["id"]))
            action, tag = "UNSUBSCRIBED", "UNSUB"
        else:
            conn.execute(
                "UPDATE leads SET status='REPLIED', reply_received=1, reply_text=?, reply_received_at=?, next_followup_at=NULL, updated_at=? WHERE id=?",
                (text, now_iso(), now_iso(), lead["id"]))
            action, tag = "REPLY_RECEIVED", "REPLY"
        conn.commit()
        log_event(conn, lead["id"], action, "OK", subject)
        handled += 1
        print(f"[{tag}] {lead['company_name']}: {text[:80]!r}")

    imap.logout()
    print(f"done, {handled} update(s)")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=3)
    main(ap.parse_args().days)
