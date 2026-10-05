"""
AI classification of replies: category, sentiment, probability (0-100) of becoming a customer, next action.

Runs on leads that have a reply but no lead_probability yet. Out-of-office replies do not stop the
follow-up sequence; everything else does (check_replies already cleared next_followup_at).

Usage:
    python scripts/classify_replies.py
"""
from ai_client import chat_json
from db import get_connection, log_event, now_iso

PROMPT_PATH = "../prompts/reply_classification_prompt.txt"
STATUS_BY_CATEGORY = {
    "INTERESTED": "INTERESTED", "QUESTION": "QUESTION", "LATER": "LATER", "REFERRAL": "QUESTION",
    "NOT_INTERESTED": "NOT_INTERESTED", "UNSUBSCRIBE": "UNSUBSCRIBED", "OTHER": "REPLIED",
}


def main() -> None:
    conn = get_connection()
    template = open(PROMPT_PATH, encoding="utf-8").read()
    rows = conn.execute(
        "SELECT * FROM leads WHERE reply_received = 1 AND reply_text IS NOT NULL AND lead_probability IS NULL"
    ).fetchall()
    print(f"{len(rows)} reply(ies) to classify")
    for lead in rows:
        prompt = (template.replace("{company_name}", lead["company_name"] or "")
                  .replace("{subject}", lead["email_subject"] or "")
                  .replace("{reply_text}", lead["reply_text"] or ""))
        try:
            r = chat_json(prompt, "reply_classification")
        except Exception as e:
            log_event(conn, lead["id"], "REPLY_CLASSIFIED", "ERROR", str(e))
            continue
        cat = str(r.get("category", "OTHER")).upper()
        prob = max(0, min(100, int(r.get("probability", 0) or 0)))
        if cat == "OUT_OF_OFFICE":
            # auto-reply: keep the sequence going, just note it
            conn.execute("UPDATE leads SET reply_received = 0, reply_category = ?, updated_at = ? WHERE id = ?",
                         (cat, now_iso(), lead["id"]))
        else:
            status = STATUS_BY_CATEGORY.get(cat, "REPLIED")
            if lead["status"] == "UNSUBSCRIBED":
                status = "UNSUBSCRIBED"
            conn.execute(
                """UPDATE leads SET reply_category = ?, reply_sentiment = ?, lead_probability = ?, reply_reasoning = ?,
                   next_action = ?, status = ?, do_not_contact = CASE WHEN ? IN ('UNSUBSCRIBED','NOT_INTERESTED') THEN 1 ELSE do_not_contact END,
                   updated_at = ? WHERE id = ?""",
                (cat, r.get("sentiment", ""), prob, r.get("reasoning", ""), r.get("next_action", ""), status, status,
                 now_iso(), lead["id"]),
            )
        conn.commit()
        log_event(conn, lead["id"], "REPLY_CLASSIFIED", "OK", f"{cat} {prob}%")
        print(f"  {lead['company_name']:<32} {cat:<15} {prob:>3}%  -> {r.get('next_action', '')}")


if __name__ == "__main__":
    main()
