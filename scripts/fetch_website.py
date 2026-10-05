"""
Fetch a small set of relevant pages from a company website and return cleaned,
truncated text for AI analysis. Never let one bad site break the pipeline.
"""
import re
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

PRIORITY_PATHS = ["", "about", "about-us", "team", "leadership", "our-team", "services", "carrier", "contact", "quote", "pricing", "faq"]
MAX_PAGES = 5
PAGE_TIMEOUT = 8
MAX_CHARS_PER_PAGE = 6000
MAX_TOTAL_CHARS = 12000

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml",
}


def _fetch_homepage(host: str):
    """Try https/http and with/without www; return (response, base_url) or raise the last error."""
    bare = host[4:] if host.startswith("www.") else host
    last = None
    for candidate in (f"https://{host}", f"https://www.{bare}", f"https://{bare}", f"http://{bare}", f"http://www.{bare}"):
        try:
            r = requests.get(candidate, headers=HEADERS, timeout=PAGE_TIMEOUT, allow_redirects=True)
            r.raise_for_status()
            return r, f"{urlparse(r.url).scheme}://{urlparse(r.url).netloc}"
        except Exception as e:
            last = e
    raise last


def _clean_text(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "nav", "footer", "noscript"]):
        tag.decompose()
    text = soup.get_text(separator=" ")
    text = re.sub(r"\s+", " ", text).strip()
    return text[:MAX_CHARS_PER_PAGE]


def _find_links(html: str, base_url: str) -> dict:
    soup = BeautifulSoup(html, "html.parser")
    found = {}
    for a in soup.find_all("a", href=True):
        href = a["href"].lower()
        for key in PRIORITY_PATHS:
            if key and key in href and key not in found:
                found[key] = urljoin(base_url, a["href"])
    return found


def research_website(website: str) -> dict:
    """
    Returns:
        {
            "status": "DONE" | "PARTIAL" | "FAILED",
            "text": "<cleaned combined text, truncated>",
            "pages_fetched": [...urls...],
            "error": "<message or None>"
        }
    """
    if not website:
        return {"status": "FAILED", "text": "", "pages_fetched": [], "error": "no website provided"}

    url = website.strip()
    if not url.startswith("http"):
        url = "https://" + url

    parsed = urlparse(url)
    base = f"{parsed.scheme}://{parsed.netloc}"

    pages_fetched = []
    combined = []

    try:
        resp, base = _fetch_homepage(parsed.netloc)
    except Exception as e:
        return {"status": "FAILED", "text": "", "pages_fetched": [], "error": f"homepage unreachable: {e}"}

    combined.append(_clean_text(resp.text))
    pages_fetched.append(base)

    links = _find_links(resp.text, base)
    for key, link_url in list(links.items())[: MAX_PAGES - 1]:
        try:
            r = requests.get(link_url, headers=HEADERS, timeout=PAGE_TIMEOUT)
            r.raise_for_status()
            combined.append(_clean_text(r.text))
            pages_fetched.append(link_url)
        except Exception:
            continue

    full_text = " ".join(combined)[:MAX_TOTAL_CHARS]

    status = "DONE" if len(pages_fetched) > 1 else "PARTIAL"
    return {"status": status, "text": full_text, "pages_fetched": pages_fetched, "error": None}
