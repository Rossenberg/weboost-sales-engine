"""Lead scoring: turns lead fields + AI analysis output into a 0-100 score."""
import re

from config import SCORE_WEIGHTS, TARGET_INDUSTRY, LEAD_PRIORITY_BANDS

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
DECISION_MAKER_TITLES = [
    "founder", "co-founder", "owner", "ceo", "president", "coo",
    "operations manager", "head of operations",
]


def priority_band(score: int) -> str:
    for lo, hi, label in LEAD_PRIORITY_BANDS:
        if lo <= score <= hi:
            return label
    return "LOW"


def compute_lead_score(lead: dict, analysis: dict) -> tuple[int, list[str]]:
    score = 0
    reasons = []
    w = SCORE_WEIGHTS

    industry = (lead.get("industry") or "").lower()
    target_terms = [t.strip() for t in TARGET_INDUSTRY.lower().split(",")]
    if any(t in industry for t in target_terms):
        score += w["target_industry_match"]
        reasons.append("Target industry match")

    if analysis.get("is_freight_broker"):
        score += w["freight_broker_confirmed"]
        reasons.append("Confirmed freight brokerage")

    role = (lead.get("contact_role") or "").lower()
    if any(t in role for t in DECISION_MAKER_TITLES):
        score += w["decision_maker_found"]
        reasons.append("Decision maker identified")

    email = lead.get("contact_email") or ""
    if EMAIL_RE.match(email):
        score += w["verified_email_format"]
        reasons.append("Valid email format")

    observed = " ".join(analysis.get("observed_features", [])).lower()
    if any(k in observed for k in ["basic", "outdated", "no automation", "simple contact form"]):
        score += w["website_outdated_or_basic"]
        reasons.append("Website appears basic/outdated")

    if "quote" not in observed and "booking" not in observed:
        score += w["no_quote_automation_observed"]
        reasons.append("No visible quote/booking automation")

    if "portal" not in observed:
        score += w["no_customer_portal_observed"]
        reasons.append("No visible customer portal")

    opportunities = analysis.get("automation_opportunities", [])
    if len(opportunities) >= 2:
        score += w["strong_automation_opportunity"]
        reasons.append("Strong automation opportunity")

    if analysis.get("personalization_fact") and len(analysis["personalization_fact"]) > 20:
        score += w["strong_personalization_fact"]
        reasons.append("Strong personalization data")

    try:
        size = int(re.sub(r"[^0-9]", "", str(lead.get("company_size") or "0")) or 0)
    except ValueError:
        size = 0
    if 5 <= size <= 200:
        score += w["company_size_in_range"]
        reasons.append("Company size in target range")

    score = min(score, 100)
    return score, reasons
