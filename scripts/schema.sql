CREATE TABLE IF NOT EXISTS leads (
    id TEXT PRIMARY KEY,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,

    company_name TEXT,
    website TEXT,
    domain TEXT,
    industry TEXT,
    company_size TEXT,
    country TEXT,
    state TEXT,
    city TEXT,

    contact_first_name TEXT,
    contact_last_name TEXT,
    contact_full_name TEXT,
    contact_role TEXT,
    contact_email TEXT,
    decision_maker_score INTEGER,
    linkedin_url TEXT,

    source TEXT,

    research_status TEXT DEFAULT 'PENDING',
    website_summary TEXT,
    business_type TEXT,
    observed_features TEXT,
    pain_points TEXT,
    automation_opportunities TEXT,
    recommended_solution TEXT,
    ai_analysis_json TEXT,

    lead_score INTEGER,
    score_reasons TEXT,

    email_subject TEXT,
    email_body TEXT,

    status TEXT DEFAULT 'NEW',

    initial_email_sent_at TEXT,
    followup_1_sent_at TEXT,
    followup_2_sent_at TEXT,
    followup_3_sent_at TEXT,
    last_contact_at TEXT,
    next_followup_at TEXT,

    reply_received INTEGER DEFAULT 0,
    reply_text TEXT,
    reply_received_at TEXT,
    reply_category TEXT,
    reply_sentiment TEXT,

    manual_notes TEXT,

    linkedin_task_status TEXT DEFAULT 'NOT_CREATED',
    linkedin_message_draft TEXT,

    meeting_booked INTEGER DEFAULT 0,
    do_not_contact INTEGER DEFAULT 0
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_leads_domain ON leads(domain) WHERE domain IS NOT NULL AND domain != '';
CREATE INDEX IF NOT EXISTS idx_leads_email ON leads(contact_email);
CREATE INDEX IF NOT EXISTS idx_leads_status ON leads(status);

CREATE TABLE IF NOT EXISTS lead_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    lead_id TEXT NOT NULL,
    timestamp TEXT NOT NULL,
    action TEXT NOT NULL,
    status TEXT NOT NULL,
    detail TEXT,
    FOREIGN KEY (lead_id) REFERENCES leads(id)
);

CREATE INDEX IF NOT EXISTS idx_events_lead ON lead_events(lead_id);
