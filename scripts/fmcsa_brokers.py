"""Pull active US freight brokers (broker authority only: no common/contract carrier authority) from the free FMCSA open data (data.transportation.gov)
and join census contact data (phone, email, officer) by DOT number.

Usage:
    python scripts/fmcsa_brokers.py --limit 5000 --states TX,FL,IL
Output:
    data/fmcsa_brokers.csv  (same columns as test_leads.csv + mc_number, dot_number, phone)
"""
import argparse
import csv
import re
import sys
from pathlib import Path

import requests

BASE = "https://data.transportation.gov/resource"
CARRIER_DS = "6eyk-hxee"  # Carrier - All With History (authority flags, name, address)
CENSUS_DS = "az4n-8mr2"  # Company Census File (phone, email, officer, fleet)
OUT = Path(__file__).resolve().parent.parent / "data" / "fmcsa_brokers.csv"

FREE_MAIL = {
    "gmail.com", "yahoo.com", "hotmail.com", "outlook.com", "aol.com", "icloud.com",
    "live.com", "msn.com", "comcast.net", "att.net", "sbcglobal.net", "me.com",
    "protonmail.com", "ymail.com", "verizon.net", "bellsouth.net", "mail.com",
}
COLUMNS = [
    "company_name", "website", "first_name", "last_name", "full_name", "job_title",
    "email", "linkedin_url", "country", "state", "city", "company_size", "industry",
    "source", "mc_number", "dot_number", "phone",
]


def soda(dataset: str, params: dict) -> list:
    r = requests.get(f"{BASE}/{dataset}.json", params=params, timeout=60)
    r.raise_for_status()
    return r.json()


def fetch_brokers(states: list, limit: int) -> list:
    where = "broker_stat='A' AND bus_ctry_code='US' AND docket_number like 'MC%' AND common_stat!='A' AND contract_stat!='A'"
    if states:
        where += " AND bus_state_code in(" + ",".join(f"'{s}'" for s in states) + ")"
    rows, offset = [], 0
    while len(rows) < limit:
        page = soda(CARRIER_DS, {
            "$where": where, "$order": "docket_number",
            "$limit": min(5000, limit - len(rows)), "$offset": offset,
        })
        if not page:
            break
        rows += page
        offset += len(page)
    return rows


def fetch_census(dots: list) -> dict:
    out = {}
    for i in range(0, len(dots), 150):
        chunk = dots[i:i + 150]
        ids = ",".join(f"'{d}'" for d in chunk)
        for row in soda(CENSUS_DS, {
            "$where": f"dot_number in({ids})",
            "$select": "dot_number,phone,email_address,company_officer_1,company_officer_2,"
                       "power_units,total_drivers,add_date,status_code",
            "$limit": 1000,
        }):
            out[row["dot_number"]] = row
    return out


def split_name(full: str):
    parts = (full or "").replace(",", " ").split()
    if not parts:
        return "", ""
    return parts[0].title(), (parts[-1].title() if len(parts) > 1 else "")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=2000)
    ap.add_argument("--states", default="")
    args = ap.parse_args()
    states = [s.strip().upper() for s in args.states.split(",") if s.strip()]

    brokers = fetch_brokers(states, args.limit)
    print(f"active brokers fetched: {len(brokers)}")
    dots = sorted({b["dot_number"].lstrip("0") for b in brokers if b.get("dot_number", "").strip("0")})
    census = fetch_census(dots)
    print(f"matched in census: {len(census)} of {len(dots)} DOT numbers")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    kept = with_email = own_domain = 0
    with open(OUT, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLUMNS)
        w.writeheader()
        for b in brokers:
            dot = b.get("dot_number", "").lstrip("0")
            c = census.get(dot)
            if not c:
                continue  # no contact data -> not useful for outreach
            email = (c.get("email_address") or "").strip().lower()
            if not email or not re.match(r"[^@\s]+@[^@\s]+\.[^@\s]+$", email):
                continue
            with_email += 1
            domain = email.split("@")[1]
            website = "" if domain in FREE_MAIL else f"https://{domain}"
            own_domain += bool(website)
            first, last = split_name(c.get("company_officer_1"))
            w.writerow({
                "company_name": (b.get("dba_name") if b.get("dba_name", "N") not in ("", "N") else b.get("legal_name", "")).title(),
                "website": website,
                "first_name": first, "last_name": last,
                "full_name": (c.get("company_officer_1") or "").title(),
                "job_title": "Company officer (FMCSA)",
                "email": email, "linkedin_url": "", "country": "USA",
                "state": b.get("bus_state_code", ""), "city": (b.get("bus_city") or "").title(),
                "company_size": c.get("total_drivers", ""), "industry": "Freight brokerage",
                "source": "fmcsa_broker_registry", "mc_number": b.get("docket_number", ""),
                "dot_number": dot, "phone": c.get("phone", ""),
            })
            kept += 1
    print(f"written {kept} rows to {OUT}")
    print(f"  with email: {with_email}; with own (non-free-mail) domain: {own_domain}")


if __name__ == "__main__":
    sys.exit(main())
