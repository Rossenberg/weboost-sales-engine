# WeBoost AI Sales Engine

Outbound engine for US freight brokers: finds brokers in the free FMCSA registry, researches each website
with AI, filters to real small/mid brokerages, writes a personal first email, sends it from our own Gmail
(after human approval), runs follow-ups, reads replies, and predicts who will become a customer.
Everything is visible in a password-protected dashboard on Cloudflare.

Plain Python + SQLite locally; dashboard is a Cloudflare Worker + D1.

## Daily run

```
.venv/bin/python scripts/run_daily.py --prospect 20
```

Order: pull approvals/rules from the dashboard → check replies → AI-classify replies → research 20 new brokers
and write emails → send follow-ups and approved emails (within the daily cap) → push everything to the dashboard.
Nothing is sent while `DRY_RUN=true` or `AUTO_SEND=false` in `.env`.

## Scripts

| Script | What it does |
|---|---|
| `fmcsa_brokers.py` | Pull active broker-only authorities from FMCSA open data → `data/fmcsa_brokers.csv` |
| `import_leads.py` | Import a CSV into the database (dedup by domain/email) |
| `ai_analysis.py` | Fetch website, AI analysis, broker/size filter, owner name, score |
| `email_generation.py` | First email in the founder's voice (+ rules from the dashboard) |
| `send_queue.py` | Follow-ups + approved first emails via Gmail, warm-up ramp, DRY_RUN |
| `check_replies.py` | IMAP: replies, bounces, unsubscribes; stops sequences |
| `classify_replies.py` | AI: reply category, probability of a deal, next step |
| `sync_dashboard.py` | Two-way sync with the dashboard |
| `approve.py` | CLI alternative to approving in the dashboard |

## Dashboard (`dashboard/`)

Cloudflare Worker with D1. Deploy: `cd dashboard && npx wrangler deploy`.
Secrets (set with `wrangler secret put`): `DASH_USER`, `DASH_PASSWORD`, `SESSION_SECRET`, `SYNC_TOKEN`.
Local `.env` needs `DASHBOARD_URL` and `DASHBOARD_SYNC_TOKEN` (= `SYNC_TOKEN`).

## Setup

```
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
cp .env.example .env   # then fill in keys
```

See `docs/DATA_MODEL.md` for the data model and `reports/` for market research.
