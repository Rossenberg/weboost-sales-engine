"""
Import leads from a CSV file into the database, skipping duplicates.

Usage:
    python scripts/import_leads.py data/test_leads.csv
"""
import csv
import sys

from db import get_connection, init_db, log_event, now_iso
from utils import normalize_domain, new_id

REQUIRED_COLUMNS = ["company_name", "website", "email"]


def import_csv(path: str) -> None:
    init_db()
    conn = get_connection()

    inserted = 0
    skipped_duplicate = 0
    skipped_invalid = 0

    with open(path, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        missing = [c for c in REQUIRED_COLUMNS if c not in reader.fieldnames]
        if missing:
            raise SystemExit(f"CSV is missing required columns: {missing}")

        for row in reader:
            company_name = (row.get("company_name") or "").strip()
            website = (row.get("website") or "").strip()
            email = (row.get("email") or "").strip().lower()

            if not company_name or (not website and not email):
                skipped_invalid += 1
                continue

            domain = normalize_domain(website)

            existing = None
            if domain:
                existing = conn.execute(
                    "SELECT id FROM leads WHERE domain = ?", (domain,)
                ).fetchone()
            if not existing and email:
                existing = conn.execute(
                    "SELECT id FROM leads WHERE lower(contact_email) = ?", (email,)
                ).fetchone()

            if existing:
                skipped_duplicate += 1
                continue

            lead_id = new_id()
            ts = now_iso()
            full_name = (row.get("full_name") or "").strip() or " ".join(
                filter(None, [row.get("first_name", "").strip(), row.get("last_name", "").strip()])
            )

            conn.execute(
                """
                INSERT INTO leads (
                    id, created_at, updated_at,
                    company_name, website, domain, industry, company_size,
                    country, state, city,
                    contact_first_name, contact_last_name, contact_full_name,
                    contact_role, contact_email, linkedin_url, source, status
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'NEW')
                """,
                (
                    lead_id, ts, ts,
                    company_name, website, domain,
                    row.get("industry", "").strip(),
                    row.get("company_size", "").strip(),
                    row.get("country", "").strip(),
                    row.get("state", "").strip(),
                    row.get("city", "").strip(),
                    row.get("first_name", "").strip(),
                    row.get("last_name", "").strip(),
                    full_name,
                    row.get("job_title", "").strip(),
                    email,
                    row.get("linkedin_url", "").strip(),
                    row.get("source", "").strip() or "csv_import",
                ),
            )
            log_event(conn, lead_id, "LEAD_IMPORTED", "OK", f"from {path}")
            inserted += 1

    conn.commit()
    conn.close()

    print(f"Imported: {inserted}")
    print(f"Skipped (duplicate): {skipped_duplicate}")
    print(f"Skipped (invalid/missing data): {skipped_invalid}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python scripts/import_leads.py <path_to_csv>")
    import_csv(sys.argv[1])
