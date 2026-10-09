"""
Fill the DEMO dashboard (weboost-demo worker, separate D1 database) with realistic sample data for
product videos. The real dashboard and the local pipeline database are never touched.

Dates are generated relative to *now*, so re-run this right before filming to keep "today" numbers right.

Usage:
    python3 scripts/demo_seed.py
"""
import random
import sqlite3
import subprocess
import tempfile
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DASH = ROOT / "dashboard"
rng = random.Random(42)
NOW = datetime.now(timezone.utc).replace(microsecond=0)
TODAY = NOW
MIN_TODAY = max(2, min(600, NOW.hour * 60 + NOW.minute - 1))  # minutes back that still fall on today (UTC)


def iso(dt):
    return dt.isoformat()


def ago(days=0, hours=0, minutes=0):
    return NOW - timedelta(days=days, hours=hours, minutes=minutes)


# ---------- names ----------
A = ["Summit", "Ridgeline", "Blue Harbor", "Iron Gate", "Prairie", "Redwood", "Lone Peak", "Silverline", "Keystone", "Northbound",
     "Cedar Point", "Granite", "Sunbelt", "Liberty Lane", "Frontier", "Crossroads", "Heartland", "Pinecrest", "Bayview", "Copperline",
     "Eagle Rock", "Trailhead", "Westgate", "Riverbend", "Highmark", "Oakline", "Stonebridge", "Clearwater", "Midway", "Patriot",
     "Arrowhead", "Lakeshore", "Big Sky", "Canyon", "Harborline", "Evergreen", "Gulfstream", "Tristate", "Coastal Plains", "Mesa"]
B = ["Logistics", "Freight", "Transport Solutions", "Freight Group", "Logistics Group", "Brokerage", "Shipping Partners", "Freight Services"]
SUF = ["LLC", "Inc", "LLC", "LLC", "Co."]
CITIES = [("Dallas", "TX"), ("Houston", "TX"), ("Chicago", "IL"), ("Atlanta", "GA"), ("Charlotte", "NC"), ("Nashville", "TN"),
          ("Columbus", "OH"), ("Indianapolis", "IN"), ("Phoenix", "AZ"), ("Denver", "CO"), ("Jacksonville", "FL"), ("Miami", "FL"),
          ("Kansas City", "MO"), ("Memphis", "TN"), ("Ontario", "CA"), ("Fort Worth", "TX"), ("Louisville", "KY"), ("Salt Lake City", "UT")]
FIRST = ["Mike", "Sarah", "Jason", "Amanda", "Chris", "Jessica", "Ryan", "Nicole", "Brian", "Megan", "Kevin", "Laura", "Tyler",
         "Ashley", "Derek", "Rachel", "Travis", "Kelly", "Marcus", "Dana"]
LAST = ["Johnson", "Miller", "Davis", "Wilson", "Anderson", "Thomas", "Moore", "Martin", "Thompson", "Garcia", "Clark", "Lewis",
        "Walker", "Hall", "Young", "King", "Wright", "Scott", "Baker", "Turner"]
FACTS = ["Saw you move flatbed and step-deck freight.", "Noticed you cover reefer lanes out of the Midwest.",
         "Saw you handle LTL and partials for manufacturers.", "Noticed your carrier page asks for active MC authority.",
         "Saw you run drayage out of the port.", "Noticed you offer same-day expedited coverage.",
         "Saw you cover dry van freight across the Southeast.", "Noticed you work with power-only and hotshot carriers."]
TYPES = ["Freight brokerage", "Freight brokerage / 3PL", "Non-asset freight brokerage", "Freight brokerage (reefer focus)",
         "Freight brokerage / drayage"]
ENDINGS = ["How are you handling carrier replies after you post a load today?",
           "I can send a 60-second screen recording showing how it works. Want me to send it?",
           "Does sorting carrier replies eat much time on your side?",
           "I'm looking for two brokerages to test it with for free. Would you be open to trying it?"]


MID = ["", "", "", "Express", "National", "Global", "American", "United", "Premier", "Prime"]


def company():
    a, m, b = rng.choice(A), rng.choice(MID), rng.choice(B)
    base = " ".join(x for x in (a, m, b) if x)
    name = f"{base} {rng.choice(SUF)}"
    dom = "".join(c for c in base.lower() if c.isalnum()) + ".com"
    return name, dom


def email_body(first, fact):
    hi = f"Hi {first}," if first else "Hi,"
    return (f"{hi}\n\n{fact}\n\nI used to dispatch and broker loads in the US, and I remember how carrier emails after posting a "
            f"load could eat into the day.\n\nAt WeBoost, I build an inbox assistant that pulls rates, equipment and availability "
            f"from carrier replies, checks FMCSA status and insurance, ranks options, and drafts responses for you to approve.\n\n"
            f"{rng.choice(ENDINGS)}\n\n— Karen\nWeBoost\nweboost.live")


FOLLOWUPS = [
    "One other detail: it works inside your existing Gmail or Outlook, so there is nothing new to install or learn.",
    "If it helps, I can run it on a week of your real carrier replies for free and show you the time it saves.",
    "I'll stop here so I don't crowd your inbox. If carrier replies ever become a bottleneck, I'm one email away.",
]

REPLIES = [  # (status, category, sentiment, probability, reply, reasoning, next action, meeting)
    ("MEETING_BOOKED", "INTERESTED", "positive", 72, "This is exactly our problem. We post 40+ loads a day and my two reps live in the inbox. Can we do a call Thursday at 2pm CT?",
     "Clear pain at high volume and they proposed a specific call time.", "Confirm Thursday 2pm CT, send calendar invite and a 1-page overview.", 1),
    ("MEETING_BOOKED", "INTERESTED", "positive", 64, "Sounds interesting. Send me the recording and some times next week.",
     "Asked for the demo video and proposed to meet next week.", "Send the 60-sec recording and three time slots for next Tue-Wed.", 1),
    ("INTERESTED", "INTERESTED", "positive", 55, "How much does it cost? We use DAT and Gmail, would it work with that?",
     "Asked about price and compatibility with their current tools: active buying interest.", "Reply with pricing and confirm DAT + Gmail support; offer a free 2-week pilot.", 0),
    ("INTERESTED", "INTERESTED", "positive", 47, "We'd be open to a free test. Who would have access to our inbox?",
     "Open to a pilot; main concern is inbox security.", "Explain read-only access and data handling; propose a 2-week pilot start date.", 0),
    ("QUESTION", "QUESTION", "neutral", 24, "Does it also check carrier insurance and safety rating, or only rates?",
     "Product question without a clear buying signal yet.", "Answer: yes, FMCSA authority, insurance and safety rating; ask about their weekly load volume.", 0),
    ("QUESTION", "REFERRAL", "neutral", 18, "I'm not the right person. Talk to our operations manager, Dana Clark.",
     "Referred to the operations manager.", "Email Dana Clark, mention the referral in the first line.", 0),
    ("LATER", "LATER", "neutral", 14, "Busy season right now. Reach out again after Thanksgiving.",
     "Interested but postponing until after the peak season.", "Schedule a follow-up for the first week of December.", 0),
    ("LATER", "LATER", "neutral", 11, "Maybe next quarter, we're switching TMS at the moment.",
     "Timing blocked by a TMS migration.", "Follow up in January once their new TMS is live.", 0),
    ("NOT_INTERESTED", "NOT_INTERESTED", "negative", 2, "We're good, we already have a process for this. Thanks.",
     "Clear no, satisfied with current process.", "No further outreach; keep in the pool for 6 months.", 0),
    ("UNSUBSCRIBED", "UNSUBSCRIBE", "negative", 0, "Please remove me from your list.",
     "Asked to stop emailing.", "Do not contact.", 0),
]


def main():
    db_path = Path(tempfile.mkdtemp()) / "demo.db"
    con = sqlite3.connect(db_path)
    con.executescript((DASH / "schema.sql").read_text())
    leads, msgs, events = [], [], []
    mid = eid = 0
    used = set()

    def new_lead(status, sent_days_ago=None, fu=0, reply=None, ready=False):
        nonlocal mid, eid
        while True:
            name, dom = company()
            if dom not in used:
                used.add(dom)
                break
        city, st = rng.choice(CITIES)
        first, last = rng.choice(FIRST), rng.choice(LAST)
        use_name = rng.random() < 0.55
        lid = str(uuid.uuid4())
        fact = rng.choice(FACTS)
        subj = rng.choice(["carrier replies after a load post", "sorting carrier replies", "How do you handle carrier replies?",
                           "after you post a load", "quick question about carrier emails"])
        body = email_body(first if use_name else "", fact)
        created = ago(days=(sent_days_ago or 0) + rng.randint(1, 3), hours=rng.randint(0, 8))
        L = dict(id=lid, company_name=name, website=f"https://{dom}", state=st, city=city,
                 contact_name=f"{first} {last}" if use_name else "", contact_role=rng.choice(["Owner", "President", "CEO", "Operations Manager"]) if use_name else "",
                 contact_email=f"{first.lower()}@{dom}" if use_name else rng.choice(["dispatch", "ops", "info"]) + f"@{dom}",
                 phone=f"{rng.randint(201, 989)}{rng.randint(2000000, 9999999)}", mc_number=f"MC{rng.randint(700000, 1650000)}",
                 status=status, research_status="DONE", lead_score=rng.choice([65, 70, 75, 75, 80, 85, 85, 90]),
                 business_type=rng.choice(TYPES), personalization_fact=fact.replace("Saw you ", "The website says they ").replace("Noticed ", ""),
                 broker_evidence="The website describes the company as a freight brokerage that works with a network of vetted carriers.",
                 company_scale="small", summary=f"{name.split(' LLC')[0]} is a {city}-based freight brokerage.",
                 email_subject=subj, email_body=body, reply_received=0, do_not_contact=0, meeting_booked=0,
                 created_at=iso(created), updated_at=iso(ago(hours=rng.randint(0, 30))))
        if sent_days_ago is not None:
            t0 = ago(days=sent_days_ago, hours=rng.randint(0, 3), minutes=rng.randint(0, 59))
            if sent_days_ago == 0:
                t0 = TODAY - timedelta(minutes=rng.randint(1, MIN_TODAY))
            L["initial_email_sent_at"] = L["last_contact_at"] = iso(t0)
            mid += 1; msgs.append(dict(id=mid, lead_id=lid, kind="initial", subject=subj, body=body, created_at=iso(t0)))
            eid += 1; events.append(dict(id=eid, lead_id=lid, timestamp=iso(t0), action="EMAIL_SENT", status="OK", detail=""))
            for n, d in zip(range(1, fu + 1), (3, 7, 12)):
                tf = t0 + timedelta(days=d)
                if tf > NOW:
                    break
                L[f"followup_{n}_sent_at"] = L["last_contact_at"] = iso(tf)
                mid += 1; msgs.append(dict(id=mid, lead_id=lid, kind=f"followup_{n}", subject="Re: " + subj, body=FOLLOWUPS[n - 1], created_at=iso(tf)))
                eid += 1; events.append(dict(id=eid, lead_id=lid, timestamp=iso(tf), action="FOLLOWUP_SENT", status="OK", detail=f"#{n}"))
            nxt = {0: 3, 1: 7, 2: 12}.get(fu)
            if nxt and status in ("SENT", "FOLLOWUP_1", "FOLLOWUP_2"):
                L["next_followup_at"] = iso(t0 + timedelta(days=nxt))
        if reply:
            st_, cat, sent_, prob, text, why, nxt_a, meet = reply
            tr = ago(days=rng.randint(0, 4), hours=rng.randint(1, 9))
            L.update(reply_received=1, reply_text=text, reply_received_at=iso(tr), reply_category=cat, reply_sentiment=sent_,
                     lead_probability=prob, reply_reasoning=why, next_action=nxt_a, meeting_booked=meet, next_followup_at=None,
                     do_not_contact=1 if st_ in ("UNSUBSCRIBED", "NOT_INTERESTED") else 0)
            mid += 1; msgs.append(dict(id=mid, lead_id=lid, kind="reply_in", subject="Re: " + subj, body=text, created_at=iso(tr)))
            eid += 1; events.append(dict(id=eid, lead_id=lid, timestamp=iso(tr), action="REPLY_CLASSIFIED", status="OK", detail=f"{cat} {prob}%"))
        leads.append(L)
        return L

    # first emails sent per day over the last 14 days (ramp-up); today's total incl. follow-ups ~85
    per_day = [14, 18, 22, 26, 30, 34, 38, 42, 46, 50, 54, 58, 62, 70]
    for i, n in enumerate(per_day):
        days = 13 - i
        for _ in range(n):
            fu = 0 if days < 3 else 1 if days < 7 else 2 if days < 12 else 3
            status = {0: "SENT", 1: "FOLLOWUP_1", 2: "FOLLOWUP_2", 3: "SEQUENCE_DONE"}[fu]
            new_lead(status, days, fu)
    # replies, bounces, follow-ups due today
    sent_leads = [l for l in leads if l["status"] != "SENT" or l.get("initial_email_sent_at", "") < iso(ago(days=1))]
    for r, l in zip(REPLIES, rng.sample(sent_leads, len(REPLIES))):
        st_, cat, sent_, prob, text, why, nxt_a, meet = r
        tr = ago(days=rng.randint(0, 4), hours=rng.randint(1, 9))
        l.update(status=st_, reply_received=1, reply_text=text, reply_received_at=iso(tr), reply_category=cat, reply_sentiment=sent_,
                 lead_probability=prob, reply_reasoning=why, next_action=nxt_a, meeting_booked=meet, next_followup_at=None,
                 do_not_contact=1 if st_ in ("UNSUBSCRIBED", "NOT_INTERESTED") else 0)
        mid += 1; msgs.append(dict(id=mid, lead_id=l["id"], kind="reply_in", subject="Re: " + l["email_subject"], body=text, created_at=iso(tr)))
        eid += 1; events.append(dict(id=eid, lead_id=l["id"], timestamp=iso(tr), action="REPLY_CLASSIFIED", status="OK", detail=f"{cat} {prob}%"))
    plain = [l for l in leads if l["status"] in ("SENT", "FOLLOWUP_1") and not l["reply_received"]]
    for l in rng.sample(plain, 6):
        l.update(status="BOUNCED", do_not_contact=1, next_followup_at=None)
    due = [l for l in leads if l["status"] in ("SENT", "FOLLOWUP_1", "FOLLOWUP_2") and l.get("next_followup_at")]
    for l in due:
        if l["next_followup_at"][:10] == TODAY.date().isoformat():
            l["next_followup_at"] = iso(TODAY + timedelta(days=1))
    for l in rng.sample(due, 4):
        l["next_followup_at"] = iso(TODAY + timedelta(hours=rng.randint(1, 5)))
    # exactly ~85 sends today: move surplus follow-ups that landed on today back to yesterday
    td = TODAY.date().isoformat()
    todays_fu = [e for e in events if e["timestamp"][:10] == td and e["action"] == "FOLLOWUP_SENT"]
    first_today = sum(1 for e in events if e["timestamp"][:10] == td and e["action"] == "EMAIL_SENT")
    by_lead = {l["id"]: l for l in leads}
    for e in todays_fu[max(0, 85 - first_today):]:
        old_ts = e["timestamp"]
        new_ts = iso(datetime.fromisoformat(old_ts) - timedelta(days=rng.randint(1, 5)))
        e["timestamp"] = new_ts
        l = by_lead[e["lead_id"]]
        for k in ("followup_1_sent_at", "followup_2_sent_at", "followup_3_sent_at", "last_contact_at"):
            if l.get(k) == old_ts:
                l[k] = new_ts
        for m in msgs:
            if m["lead_id"] == e["lead_id"] and m["created_at"] == old_ts:
                m["created_at"] = new_ts
    # follow-ups already sent today: top up to 85 sends today
    today_sent = sum(1 for e in events if e["timestamp"][:10] == TODAY.date().isoformat() and e["action"] in ("EMAIL_SENT", "FOLLOWUP_SENT"))
    pool = [l for l in leads if l["status"] in ("FOLLOWUP_1", "FOLLOWUP_2") and not l["reply_received"]]
    for l in rng.sample(pool, max(0, 85 - today_sent)):
        t = TODAY - timedelta(minutes=rng.randint(1, MIN_TODAY))
        eid += 1; events.append(dict(id=eid, lead_id=l["id"], timestamp=iso(t), action="FOLLOWUP_SENT", status="OK", detail="#1"))
    # awaiting approval + approved
    for _ in range(14):
        new_lead("READY")
    for _ in range(3):
        new_lead("APPROVED")

    cols = ["id", "company_name", "website", "state", "city", "contact_name", "contact_role", "contact_email", "phone", "mc_number", "status",
            "research_status", "lead_score", "business_type", "personalization_fact", "broker_evidence", "company_scale", "summary",
            "email_subject", "email_body", "initial_email_sent_at", "followup_1_sent_at", "followup_2_sent_at", "followup_3_sent_at",
            "next_followup_at", "last_contact_at", "reply_received", "reply_text", "reply_received_at", "reply_category", "reply_sentiment",
            "lead_probability", "reply_reasoning", "next_action", "do_not_contact", "meeting_booked", "created_at", "updated_at"]
    con.executemany(f"INSERT INTO leads ({','.join(cols)}) VALUES ({','.join('?' * len(cols))})", [[l.get(c) for c in cols] for l in leads])
    con.executemany("INSERT INTO messages VALUES (:id,:lead_id,:kind,:subject,:body,:created_at)", msgs)
    con.executemany("INSERT INTO events VALUES (:id,:lead_id,:timestamp,:action,:status,:detail)", events)

    # AI costs: ~$6 this month, ~$0.30 today, split by step
    usage, uid = [], 0
    split = {"analysis": 0.56, "email": 0.28, "followup": 0.11, "reply_classification": 0.05}
    month_days = max(1, NOW.day)
    weights = [rng.uniform(0.6, 1.4) for _ in range(month_days - 1)]
    for d in range(month_days):
        day_total = 0.30 if d == 0 else 5.75 * weights[d - 1] / sum(weights)
        for step, share in split.items():
            cost = day_total * share
            per_call = {"analysis": 0.0034, "email": 0.0016, "followup": 0.0009, "reply_classification": 0.0011}[step]
            calls = max(1, round(cost / per_call))
            for _ in range(calls):
                uid += 1
                c = cost / calls
                tin = int(c / (0.10 + 0.5 * 0.16) * 1e6)
                usage.append((uid, iso(TODAY - timedelta(days=d, minutes=rng.randint(0, MIN_TODAY))), step, "gpt-6-luna", tin, int(tin * 0.16), round(c, 6)))
    con.executemany("INSERT INTO api_usage VALUES (?,?,?,?,?,?,?)", usage)

    meta = {"pool_total": "15574", "pool_imported": "1240", "dry_run": "false", "daily_cap": "90", "daily_limit": "90",
            "send_start_date": (NOW - timedelta(days=14)).date().isoformat(), "last_sync": iso(NOW - timedelta(minutes=3))}
    con.executemany("INSERT INTO meta VALUES (?,?)", meta.items())
    rules = ["Keep emails under 80 words.", "Never use the words 'game-changer' or 'revolutionary'.",
             "Mention that it works with DAT and Truckstop.", "Lead with the fraud check when the website mentions carrier vetting."]
    con.executemany("INSERT INTO rules (created_at, text, active) VALUES (?,?,1)", [(iso(ago(days=10 - i * 2)), r) for i, r in enumerate(rules)])
    notes = [("approve", "Good, but make the opening line shorter."), ("reject", "This company is a carrier, not a broker."),
             ("approve", "Great personalization, keep this style."), ("reject", "Too long, cut the second paragraph.")]
    sample = rng.sample([l for l in leads if l.get("initial_email_sent_at")], len(notes))
    con.executemany("INSERT INTO actions (created_at, lead_id, action, note, synced) VALUES (?,?,?,?,1)",
                    [(iso(ago(days=i + 1)), l["id"], a, n) for i, ((a, n), l) in enumerate(zip(notes, sample))])
    con.commit()

    sql = ["DELETE FROM leads;", "DELETE FROM messages;", "DELETE FROM events;", "DELETE FROM api_usage;", "DELETE FROM meta;",
           "DELETE FROM rules;", "DELETE FROM actions;"]
    sql += [line for line in con.iterdump() if line.startswith("INSERT INTO")]
    out = Path(tempfile.mkdtemp()) / "demo_seed.sql"
    out.write_text("\n".join(sql))
    print(f"leads {len(leads)}, messages {len(msgs)}, events {len(events)}, usage rows {len(usage)} -> uploading")
    subprocess.run(["npx", "--yes", "wrangler@latest", "d1", "execute", "weboost-demo", "--env", "demo", "--remote", "--file", str(out), "--yes"],
                   cwd=DASH, check=True, stdout=subprocess.DEVNULL)
    print("demo data loaded: https://weboost-demo.gasparyaninvest.workers.dev")


if __name__ == "__main__":
    main()
