"""
One daily run of the whole engine, in a safe order:

  1. sync pull   - take approvals / edits / AI rules from the dashboard
  2. replies     - read the mailbox, stop sequences for people who answered, catch bounces/unsubscribes
  3. classify    - AI reads replies: category, probability, next step
  4. prospect    - research N new brokers and write first emails (they wait for approval in the dashboard)
  5. send        - follow-ups + approved first emails, within today's cap (DRY_RUN respected)
  6. sync push   - send everything to the dashboard

Usage:
    python scripts/run_daily.py [--prospect 20] [--skip-send]
"""
import argparse
import os
import traceback
from pathlib import Path

os.chdir(Path(__file__).resolve().parent)  # prompts are loaded with paths relative to scripts/

import ai_analysis
import check_replies
import classify_replies
import email_generation
import send_queue
import sync_dashboard
from config import DASHBOARD_URL, GMAIL_APP_PASSWORD


def step(name, fn, *args):
    print(f"\n=== {name} ===")
    try:
        fn(*args)
    except SystemExit as e:
        print(f"skipped: {e}")
    except Exception:
        traceback.print_exc()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--prospect", type=int, default=20, help="how many NEW leads to research per run")
    ap.add_argument("--skip-send", action="store_true")
    args = ap.parse_args()

    if DASHBOARD_URL:
        step("sync: pull from dashboard", lambda: sync_dashboard.pull(sync_dashboard.get_connection()))
    if GMAIL_APP_PASSWORD:
        step("check replies", check_replies.main, 7)
    step("classify replies", classify_replies.main)
    if args.prospect:
        step("research new leads", ai_analysis.main, args.prospect)
        step("write first emails", email_generation.main, args.prospect)
    if not args.skip_send:
        step("send", send_queue.main, 50)
    if DASHBOARD_URL:
        step("sync: push to dashboard", lambda: sync_dashboard.push(sync_dashboard.get_connection()))


if __name__ == "__main__":
    main()
