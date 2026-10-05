// WeBoost Sales Engine dashboard: login, read-only analytics over D1, approve/reject actions,
// AI-training rules, and a token-protected sync API for the local Python pipeline.
import PAGE from "./ui.html";
import LOGIN from "./login.html";

const enc = new TextEncoder();
const SESSION_DAYS = 14;

// ---------- auth ----------
const b64url = (buf) => btoa(String.fromCharCode(...new Uint8Array(buf))).replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, "");

async function hmac(secret, data) {
  const key = await crypto.subtle.importKey("raw", enc.encode(secret), { name: "HMAC", hash: "SHA-256" }, false, ["sign"]);
  return b64url(await crypto.subtle.sign("HMAC", key, enc.encode(data)));
}

function safeEqual(a, b) {
  if (typeof a !== "string" || typeof b !== "string" || a.length !== b.length) return false;
  let r = 0;
  for (let i = 0; i < a.length; i++) r |= a.charCodeAt(i) ^ b.charCodeAt(i);
  return r === 0;
}

async function makeSession(env, user) {
  const payload = `${user}|${Date.now() + SESSION_DAYS * 864e5}`;
  return `${btoa(payload)}.${await hmac(env.SESSION_SECRET, payload)}`;
}

async function isLoggedIn(req, env) {
  const m = (req.headers.get("Cookie") || "").match(/wb_session=([^;]+)/);
  if (!m) return false;
  const [p, sig] = m[1].split(".");
  let payload;
  try { payload = atob(p); } catch { return false; }
  if (!safeEqual(await hmac(env.SESSION_SECRET, payload), sig || "")) return false;
  return Number(payload.split("|")[1]) > Date.now();
}

function hasSyncToken(req, env) {
  const t = (req.headers.get("Authorization") || "").replace(/^Bearer\s+/i, "");
  return env.SYNC_TOKEN && safeEqual(t, env.SYNC_TOKEN);
}

// ---------- helpers ----------
const json = (data, status = 200) => new Response(JSON.stringify(data), { status, headers: { "content-type": "application/json; charset=utf-8", "cache-control": "no-store" } });
const html = (body, status = 200, headers = {}) => new Response(body, { status, headers: { "content-type": "text/html; charset=utf-8", "cache-control": "no-store", ...headers } });
const all = (env, sql, ...b) => env.DB.prepare(sql).bind(...b).all().then((r) => r.results);
const first = (env, sql, ...b) => env.DB.prepare(sql).bind(...b).first();
const nowIso = () => new Date().toISOString();

const LEAD_COLS = ["id", "company_name", "website", "state", "city", "contact_name", "contact_role", "contact_email", "phone", "mc_number",
  "status", "research_status", "lead_score", "business_type", "personalization_fact", "broker_evidence", "company_scale", "summary",
  "email_subject", "email_body", "initial_email_sent_at", "followup_1_sent_at", "followup_2_sent_at", "followup_3_sent_at",
  "next_followup_at", "last_contact_at", "reply_received", "reply_text", "reply_received_at", "reply_category", "reply_sentiment",
  "lead_probability", "reply_reasoning", "next_action", "do_not_contact", "meeting_booked", "created_at", "updated_at"];

function upsertStatements(env, table, cols, rows) {
  const sql = `INSERT OR REPLACE INTO ${table} (${cols.join(",")}) VALUES (${cols.map(() => "?").join(",")})`;
  const stmt = env.DB.prepare(sql);
  return rows.map((r) => stmt.bind(...cols.map((c) => (r[c] === undefined ? null : r[c]))));
}

async function runBatched(env, statements, size = 80) {
  for (let i = 0; i < statements.length; i += size) await env.DB.batch(statements.slice(i, i + size));
}

// ---------- sync API (local pipeline <-> cloud) ----------
async function syncPush(req, env) {
  const d = await req.json();
  const st = [];
  if (d.full_leads) st.push(env.DB.prepare("DELETE FROM leads"));
  st.push(...upsertStatements(env, "leads", LEAD_COLS, d.leads || []));
  st.push(...upsertStatements(env, "messages", ["id", "lead_id", "kind", "subject", "body", "created_at"], d.messages || []));
  st.push(...upsertStatements(env, "events", ["id", "lead_id", "timestamp", "action", "status", "detail"], d.events || []));
  st.push(...upsertStatements(env, "api_usage", ["id", "created_at", "step", "model", "input_tokens", "output_tokens", "cost_usd"], d.usage || []));
  const meta = { ...(d.meta || {}), last_sync: nowIso() };
  st.push(...upsertStatements(env, "meta", ["key", "value"], Object.entries(meta).map(([key, value]) => ({ key, value: String(value) }))));
  await runBatched(env, st);
  return json({ ok: true, leads: (d.leads || []).length });
}

async function syncPull(env) {
  const actions = await all(env, "SELECT * FROM actions WHERE synced = 0 ORDER BY id");
  const rules = await all(env, "SELECT id, text FROM rules WHERE active = 1 ORDER BY id");
  return json({ actions, rules });
}

async function syncAck(req, env) {
  const { ids = [] } = await req.json();
  if (ids.length) await runBatched(env, ids.map((id) => env.DB.prepare("UPDATE actions SET synced = 1 WHERE id = ?").bind(id)));
  return json({ ok: true });
}

// ---------- dashboard API ----------
async function dashboardData(env) {
  const today = nowIso().slice(0, 10);
  const month = today.slice(0, 7);
  const since14 = new Date(Date.now() - 13 * 864e5).toISOString().slice(0, 10);
  const endOfToday = `${today}T23:59:59`;

  const [statusRows, meta, sentToday, perDay, usageTotals, usageByStep, usageByDay, rules, pending, feedback, leads] = await Promise.all([
    all(env, "SELECT status, COUNT(*) n FROM leads GROUP BY status"),
    all(env, "SELECT key, value FROM meta"),
    first(env, "SELECT COUNT(*) n FROM events WHERE action IN ('EMAIL_SENT','FOLLOWUP_SENT') AND status='OK' AND timestamp >= ?", today),
    all(env, `SELECT substr(timestamp,1,10) d, SUM(action='EMAIL_SENT') first, SUM(action='FOLLOWUP_SENT') followup
              FROM events WHERE status='OK' AND action IN ('EMAIL_SENT','FOLLOWUP_SENT') AND timestamp >= ? GROUP BY d ORDER BY d`, since14),
    first(env, `SELECT COALESCE(SUM(cost_usd),0) total,
                COALESCE(SUM(CASE WHEN created_at >= ? THEN cost_usd END),0) today,
                COALESCE(SUM(CASE WHEN substr(created_at,1,7) = ? THEN cost_usd END),0) month,
                COALESCE(SUM(input_tokens+output_tokens),0) tokens, COUNT(*) calls FROM api_usage`, today, month),
    all(env, "SELECT step, COUNT(*) calls, SUM(input_tokens) tin, SUM(output_tokens) tout, SUM(cost_usd) cost FROM api_usage GROUP BY step ORDER BY cost DESC"),
    all(env, "SELECT substr(created_at,1,10) d, SUM(cost_usd) cost FROM api_usage WHERE created_at >= ? GROUP BY d ORDER BY d", since14),
    all(env, "SELECT id, text, created_at FROM rules WHERE active = 1 ORDER BY id DESC"),
    all(env, "SELECT lead_id, action FROM actions WHERE synced = 0"),
    all(env, "SELECT a.created_at, a.action, a.note, l.company_name FROM actions a LEFT JOIN leads l ON l.id = a.lead_id WHERE a.note IS NOT NULL AND a.note != '' ORDER BY a.id DESC LIMIT 30"),
    all(env, `SELECT ${LEAD_COLS.join(",")} FROM leads ORDER BY COALESCE(lead_probability,-1) DESC, lead_score DESC`),
  ]);

  const followupsDueToday = leads.filter((l) => ["SENT", "FOLLOWUP_1", "FOLLOWUP_2"].includes(l.status) && !l.reply_received && !l.do_not_contact && l.next_followup_at && l.next_followup_at <= endOfToday).length;
  return { today, meta: Object.fromEntries(meta.map((m) => [m.key, m.value])), statuses: Object.fromEntries(statusRows.map((r) => [r.status, r.n])),
    sentToday: sentToday?.n || 0, followupsDueToday, perDay, usage: { ...usageTotals, byStep: usageByStep, byDay: usageByDay }, rules, pending, feedback, leads };
}

async function leadDetail(env, id) {
  const [lead, messages, events] = await Promise.all([
    first(env, "SELECT * FROM leads WHERE id = ?", id),
    all(env, "SELECT kind, subject, body, created_at FROM messages WHERE lead_id = ? ORDER BY created_at", id),
    all(env, "SELECT timestamp, action, status, detail FROM events WHERE lead_id = ? ORDER BY timestamp DESC LIMIT 60", id),
  ]);
  if (!lead) return json({ error: "not found" }, 404);
  return json({ lead, messages, events });
}

const ALLOWED_ACTIONS = new Set(["approve", "reject", "edit_approve", "meeting", "dnc", "note", "reopen"]);

async function addAction(req, env) {
  const a = await req.json();
  if (!ALLOWED_ACTIONS.has(a.action) || !a.lead_id) return json({ error: "bad action" }, 400);
  await env.DB.prepare("INSERT INTO actions (created_at, lead_id, action, subject, body, note) VALUES (?, ?, ?, ?, ?, ?)")
    .bind(nowIso(), a.lead_id, a.action, a.subject || null, a.body || null, a.note || null).run();
  // reflect the change in the cloud copy right away so the UI updates before the next sync
  const statusFor = { approve: "APPROVED", edit_approve: "APPROVED", reject: "REJECTED", reopen: "READY" }[a.action];
  if (statusFor) await env.DB.prepare("UPDATE leads SET status = ?, updated_at = ? WHERE id = ?").bind(statusFor, nowIso(), a.lead_id).run();
  if (a.action === "edit_approve") await env.DB.prepare("UPDATE leads SET email_subject = ?, email_body = ? WHERE id = ?").bind(a.subject, a.body, a.lead_id).run();
  if (a.action === "meeting") await env.DB.prepare("UPDATE leads SET meeting_booked = 1, status = 'MEETING_BOOKED' WHERE id = ?").bind(a.lead_id).run();
  if (a.action === "dnc") await env.DB.prepare("UPDATE leads SET do_not_contact = 1 WHERE id = ?").bind(a.lead_id).run();
  if (a.make_rule && a.note) await env.DB.prepare("INSERT INTO rules (created_at, text) VALUES (?, ?)").bind(nowIso(), a.note).run();
  return json({ ok: true });
}

// ---------- router ----------
export default {
  async fetch(req, env) {
    const url = new URL(req.url);
    const path = url.pathname;

    if (path.startsWith("/api/sync/")) {
      if (!hasSyncToken(req, env)) return json({ error: "unauthorized" }, 401);
      if (path === "/api/sync/push" && req.method === "POST") return syncPush(req, env);
      if (path === "/api/sync/pull" && req.method === "GET") return syncPull(env);
      if (path === "/api/sync/ack" && req.method === "POST") return syncAck(req, env);
      return json({ error: "not found" }, 404);
    }

    if (path === "/login") {
      if (req.method === "POST") {
        const f = await req.formData();
        const ok = safeEqual(String(f.get("user") || ""), env.DASH_USER || "") && safeEqual(String(f.get("password") || ""), env.DASH_PASSWORD || "");
        if (!ok) return html(LOGIN.replace("<!--ERR-->", '<p class="err">Неверный логин или пароль</p>'), 401);
        const cookie = `wb_session=${await makeSession(env, env.DASH_USER)}; Path=/; HttpOnly; Secure; SameSite=Lax; Max-Age=${SESSION_DAYS * 86400}`;
        return new Response(null, { status: 303, headers: { Location: "/", "Set-Cookie": cookie } });
      }
      return html(LOGIN);
    }
    if (path === "/logout") return new Response(null, { status: 303, headers: { Location: "/login", "Set-Cookie": "wb_session=; Path=/; Max-Age=0" } });

    if (!(await isLoggedIn(req, env))) {
      return path.startsWith("/api/") ? json({ error: "unauthorized" }, 401) : Response.redirect(`${url.origin}/login`, 303);
    }

    if (path === "/" ) return html(PAGE);
    if (path === "/api/data") return json(await dashboardData(env));
    if (path.startsWith("/api/lead/")) return leadDetail(env, decodeURIComponent(path.slice(10)));
    if (path === "/api/action" && req.method === "POST") return addAction(req, env);
    if (path === "/api/rules" && req.method === "POST") {
      const { text } = await req.json();
      if (!text || !text.trim()) return json({ error: "empty" }, 400);
      await env.DB.prepare("INSERT INTO rules (created_at, text) VALUES (?, ?)").bind(nowIso(), text.trim()).run();
      return json({ ok: true });
    }
    if (path.startsWith("/api/rules/") && req.method === "DELETE") {
      await env.DB.prepare("UPDATE rules SET active = 0 WHERE id = ?").bind(Number(path.slice(11))).run();
      return json({ ok: true });
    }
    return json({ error: "not found" }, 404);
  },
};
