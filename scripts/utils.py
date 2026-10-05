"""Shared helper functions."""
import re
import uuid


def normalize_domain(website: str) -> str:
    """https://www.company.com/ -> company.com"""
    if not website:
        return ""
    w = website.strip().lower()
    w = re.sub(r"^https?://", "", w)
    w = re.sub(r"^www\.", "", w)
    w = w.split("/")[0]
    return w.strip()


def new_id() -> str:
    return str(uuid.uuid4())
