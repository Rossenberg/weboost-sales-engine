"""
Human approval step: review generated emails and mark them APPROVED (only APPROVED leads are sent).

Usage:
    python scripts/approve.py --list              # show READY emails
    python scripts/approve.py --ids <id> <id>     # approve specific leads (id prefix is enough)
    python scripts/approve.py --all               # approve every READY lead
"""
import argparse

from db import get_connection, log_event, now_iso


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--ids", nargs="*", default=[])
    args = ap.parse_args()

    conn = get_connection()
    ready = conn.execute("SELECT * FROM leads WHERE status = 'READY' ORDER BY lead_score DESC").fetchall()

    if args.list or not (args.all or args.ids):
        for r in ready:
            print(f"--- {r['id'][:8]} | {r['company_name']} | score {r['lead_score']} | to {r['contact_email']}")
            print(f"Subject: {r['email_subject']}\n{r['email_body']}\n")
        print(f"{len(ready)} READY lead(s)")
        return

    chosen = ready if args.all else [r for r in ready if any(r["id"].startswith(p) for p in args.ids)]
    for r in chosen:
        conn.execute("UPDATE leads SET status='APPROVED', updated_at=? WHERE id=?", (now_iso(), r["id"]))
        log_event(conn, r["id"], "EMAIL_APPROVED", "OK", "")
    conn.commit()
    print(f"approved {len(chosen)} lead(s)")


if __name__ == "__main__":
    main()
