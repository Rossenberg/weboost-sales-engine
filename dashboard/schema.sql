-- Cloud copy of the local pipeline data (pushed by scripts/sync_dashboard.py) + dashboard-side actions.
CREATE TABLE IF NOT EXISTS leads (
  id TEXT PRIMARY KEY, company_name TEXT, website TEXT, state TEXT, city TEXT,
  contact_name TEXT, contact_role TEXT, contact_email TEXT, phone TEXT, mc_number TEXT,
  status TEXT, research_status TEXT, lead_score INTEGER, business_type TEXT,
  personalization_fact TEXT, broker_evidence TEXT, company_scale TEXT, summary TEXT,
  email_subject TEXT, email_body TEXT,
  initial_email_sent_at TEXT, followup_1_sent_at TEXT, followup_2_sent_at TEXT, followup_3_sent_at TEXT,
  next_followup_at TEXT, last_contact_at TEXT,
  reply_received INTEGER DEFAULT 0, reply_text TEXT, reply_received_at TEXT,
  reply_category TEXT, reply_sentiment TEXT, lead_probability INTEGER, reply_reasoning TEXT, next_action TEXT,
  do_not_contact INTEGER DEFAULT 0, meeting_booked INTEGER DEFAULT 0,
  created_at TEXT, updated_at TEXT
);
CREATE INDEX IF NOT EXISTS idx_leads_status ON leads(status);
CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY, lead_id TEXT, kind TEXT, subject TEXT, body TEXT, created_at TEXT);
CREATE INDEX IF NOT EXISTS idx_msg_lead ON messages(lead_id);
CREATE TABLE IF NOT EXISTS events (id INTEGER PRIMARY KEY, lead_id TEXT, timestamp TEXT, action TEXT, status TEXT, detail TEXT);
CREATE INDEX IF NOT EXISTS idx_ev_lead ON events(lead_id);
CREATE INDEX IF NOT EXISTS idx_ev_ts ON events(timestamp);
CREATE TABLE IF NOT EXISTS api_usage (id INTEGER PRIMARY KEY, created_at TEXT, step TEXT, model TEXT, input_tokens INTEGER, output_tokens INTEGER, cost_usd REAL);
CREATE TABLE IF NOT EXISTS meta (key TEXT PRIMARY KEY, value TEXT);
-- written by the dashboard, pulled by the local pipeline
CREATE TABLE IF NOT EXISTS actions (
  id INTEGER PRIMARY KEY AUTOINCREMENT, created_at TEXT, lead_id TEXT, action TEXT,
  subject TEXT, body TEXT, note TEXT, synced INTEGER DEFAULT 0
);
CREATE TABLE IF NOT EXISTS rules (id INTEGER PRIMARY KEY AUTOINCREMENT, created_at TEXT, text TEXT, active INTEGER DEFAULT 1);
