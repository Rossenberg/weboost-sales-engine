# Data Model — WeBoost AI Sales Engine

MVP storage: local SQLite file (`data/weboost.db`). Same schema will move to Supabase
(Postgres) unchanged when we go to production — no redesign needed later.

## Table: leads

| Field                      | Type      | Notes                                             |
|-----------------------------|-----------|----------------------------------------------------|
| id                          | TEXT PK   | UUID, stable unique id                             |
| created_at                  | TEXT      | ISO timestamp                                      |
| updated_at                  | TEXT      | ISO timestamp                                      |
| company_name                | TEXT      |                                                     |
| website                     | TEXT      | raw, as imported                                   |
| domain                      | TEXT      | normalized (no protocol/www/trailing slash) — used for dedup |
| industry                    | TEXT      |                                                     |
| company_size                | TEXT      |                                                     |
| country                     | TEXT      |                                                     |
| state                       | TEXT      |                                                     |
| city                        | TEXT      |                                                     |
| contact_first_name          | TEXT      |                                                     |
| contact_last_name           | TEXT      |                                                     |
| contact_full_name           | TEXT      |                                                     |
| contact_role                | TEXT      |                                                     |
| contact_email               | TEXT      |                                                     |
| decision_maker_score        | INTEGER   |                                                     |
| linkedin_url                | TEXT      |                                                     |
| source                      | TEXT      | e.g. "csv_import_2026-09-24"                       |
| research_status             | TEXT      | PENDING / PARTIAL / DONE / FAILED                  |
| website_summary             | TEXT      |                                                     |
| business_type               | TEXT      |                                                     |
| observed_features           | TEXT(JSON)|                                                     |
| pain_points                 | TEXT(JSON)|                                                     |
| automation_opportunities    | TEXT(JSON)|                                                     |
| recommended_solution        | TEXT      |                                                     |
| ai_analysis_json            | TEXT(JSON)| full structured AI output, raw                     |
| lead_score                  | INTEGER   | 0-100                                              |
| score_reasons               | TEXT(JSON)|                                                     |
| email_subject                | TEXT      |                                                     |
| email_body                   | TEXT      |                                                     |
| status                      | TEXT      | see state machine below                            |
| initial_email_sent_at        | TEXT      |                                                     |
| followup_1_sent_at           | TEXT      |                                                     |
| followup_2_sent_at           | TEXT      |                                                     |
| followup_3_sent_at           | TEXT      |                                                     |
| last_contact_at              | TEXT      |                                                     |
| next_followup_at             | TEXT      |                                                     |
| reply_received               | INTEGER   | 0/1                                                 |
| reply_text                   | TEXT      |                                                     |
| reply_received_at            | TEXT      |                                                     |
| reply_category               | TEXT      |                                                     |
| reply_sentiment               | TEXT      |                                                     |
| manual_notes                 | TEXT      |                                                     |
| linkedin_task_status          | TEXT      | NOT_CREATED / READY / SENT_MANUALLY / REPLIED / SKIPPED |
| linkedin_message_draft        | TEXT      |                                                     |
| meeting_booked                | INTEGER   | 0/1                                                 |
| do_not_contact                | INTEGER   | 0/1                                                 |

## Table: lead_events (log, append-only)

| Field       | Type    | Notes                                                  |
|-------------|---------|---------------------------------------------------------|
| id          | INTEGER PK AUTOINCREMENT |                                          |
| lead_id     | TEXT    | FK -> leads.id                                          |
| timestamp   | TEXT    | ISO timestamp                                            |
| action      | TEXT    | WEBSITE_FETCHED / AI_ANALYSIS_COMPLETED / EMAIL_GENERATED / EMAIL_SENT / REPLY_RECEIVED / REPLY_CLASSIFIED / FOLLOWUP_SENT / ERROR |
| status      | TEXT    | OK / ERROR                                               |
| detail      | TEXT    | free text / error message                                |

## Status state machine (leads.status)

```
NEW -> RESEARCHING -> RESEARCHED -> READY -> APPROVED -> SENT
SENT -> FOLLOWUP_1 -> FOLLOWUP_2 -> FOLLOWUP_3
(any sent state) -> REPLIED -> INTERESTED | QUESTION | LATER | NOT_INTERESTED | UNSUBSCRIBED
SENT/FOLLOWUP_* -> BOUNCED | INVALID_EMAIL
INTERESTED -> MEETING_BOOKED -> CUSTOMER
(any) -> PAUSED
(any) -> ERROR
```

Invalid transitions (e.g. sending a follow-up on a lead already REPLIED, UNSUBSCRIBED,
BOUNCED or PAUSED) are blocked in code before any send happens.

## Deduplication rule

A new CSV row is treated as a duplicate of an existing lead if either matches:
- normalized `domain` is identical, OR
- `contact_email` is identical (case-insensitive)

Duplicates are not inserted as a second active row; they are logged and skipped.
