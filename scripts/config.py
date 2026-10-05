"""Central configuration. All tunable knobs live here, not scattered in scripts."""
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")

# --- AI ---
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
AI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

# --- Safety ---
DRY_RUN = os.getenv("DRY_RUN", "true").lower() == "true"
TEST_EMAIL = os.getenv("TEST_EMAIL", "")
AUTO_SEND = os.getenv("AUTO_SEND", "false").lower() == "true"
DAILY_SEND_LIMIT = int(os.getenv("DAILY_SEND_LIMIT", "30"))

# --- Targeting ---
TARGET_INDUSTRY = os.getenv("TARGET_INDUSTRY", "logistics,3pl,fulfillment,warehousing,brokerage,freight")
TARGET_COUNTRY = os.getenv("TARGET_COUNTRY", "USA")

# --- Scoring (0-100). Weights are additive; tune freely. ---
SCORE_WEIGHTS = {
    "target_industry_match": 10,
    "freight_broker_confirmed": 25,
    "decision_maker_found": 10,
    "verified_email_format": 10,
    "website_outdated_or_basic": 10,
    "no_quote_automation_observed": 10,
    "no_customer_portal_observed": 10,
    "strong_automation_opportunity": 15,
    "strong_personalization_fact": 5,
    "company_size_in_range": 10,
}

LEAD_PRIORITY_BANDS = [
    (75, 100, "HIGH"),
    (60, 74, "GOOD"),
    (40, 59, "MEDIUM"),
    (0, 39, "LOW"),
]
HIGH_VALUE_SCORE = int(os.getenv("HIGH_VALUE_SCORE", "75"))
MIN_LEAD_SCORE = int(os.getenv("MIN_LEAD_SCORE", "40"))

# --- Follow-up timing (days after initial send) ---
FOLLOWUP_1_DAYS = int(os.getenv("FOLLOWUP_1_DAYS", "3"))
FOLLOWUP_2_DAYS = int(os.getenv("FOLLOWUP_2_DAYS", "7"))
FOLLOWUP_3_DAYS = int(os.getenv("FOLLOWUP_3_DAYS", "12"))

# --- Sender / booking ---
SENDER_NAME = os.getenv("SENDER_NAME", "Karen")
SENDER_EMAIL = os.getenv("SENDER_EMAIL", "")
REPLY_TO = os.getenv("REPLY_TO", SENDER_EMAIL)
BOOKING_URL = os.getenv("BOOKING_URL", "")

# --- Notifications ---
NOTIFICATION_CHANNEL = os.getenv("NOTIFICATION_CHANNEL", "dashboard")

# --- Own sender (Gmail SMTP/IMAP with an app password; secrets live in .env only) ---
GMAIL_USER = os.getenv("GMAIL_USER", "")  # e.g. karen@getweboost.com
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD", "").replace(" ", "").strip("\"'")
SENDER_POSTAL_ADDRESS = os.getenv("SENDER_POSTAL_ADDRESS", "")  # required by CAN-SPAM in every email
SEND_START_DATE = os.getenv("SEND_START_DATE", "")  # YYYY-MM-DD, first day of cold sending (after warm-up)
# Per-mailbox daily cap by day since SEND_START_DATE: (from_day, max_per_day). Last matching row wins.
SEND_RAMP = [(0, 5), (7, 10), (14, 15), (21, 20), (35, 25)]
SEND_DELAY_SECONDS = (60, 180)  # random pause between two sends
SENDER_BACKGROUND = os.getenv("SENDER_BACKGROUND", "I used to work as a dispatcher and freight broker in the US.")

# --- AI pricing for cost tracking (USD per 1M tokens; set to your model's real prices) ---
AI_PRICE_IN_PER_M = float(os.getenv("AI_PRICE_IN_PER_M", "0.10"))
AI_PRICE_OUT_PER_M = float(os.getenv("AI_PRICE_OUT_PER_M", "0.50"))

# --- Dashboard sync ---
DASHBOARD_URL = os.getenv("DASHBOARD_URL", "")
DASHBOARD_SYNC_TOKEN = os.getenv("DASHBOARD_SYNC_TOKEN", "")
STYLE_RULES_PATH = ROOT / "prompts" / "style_rules.txt"  # written by sync from dashboard "AI training"
