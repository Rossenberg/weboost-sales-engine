"""Low-level Gmail SMTP sender. Plain-text only, CAN-SPAM footer, List-Unsubscribe header."""
import smtplib
from email.message import EmailMessage
from email.utils import formataddr, make_msgid

from config import GMAIL_APP_PASSWORD, GMAIL_USER, SENDER_NAME, SENDER_POSTAL_ADDRESS

FOOTER = (
    "\n\n--\n{address}\n"
    "If you'd rather not hear from me, just reply \"unsubscribe\" and I won't write again."
)


def build_message(to_email: str, subject: str, body: str, in_reply_to: str = "") -> EmailMessage:
    msg = EmailMessage()
    msg["From"] = formataddr((SENDER_NAME, GMAIL_USER))
    msg["To"] = to_email
    msg["Subject"] = subject
    msg["Message-ID"] = make_msgid(domain=GMAIL_USER.split("@")[-1] or "localhost")
    msg["List-Unsubscribe"] = f"<mailto:{GMAIL_USER}?subject=unsubscribe>"
    if in_reply_to:
        msg["In-Reply-To"] = in_reply_to
        msg["References"] = in_reply_to
    msg.set_content(body.rstrip() + FOOTER.format(address=SENDER_POSTAL_ADDRESS))
    return msg


def send(msg: EmailMessage) -> str:
    """Send via Gmail SMTP and return the Message-ID."""
    if not GMAIL_USER or not GMAIL_APP_PASSWORD:
        raise RuntimeError("GMAIL_USER / GMAIL_APP_PASSWORD are not set in .env")
    if not SENDER_POSTAL_ADDRESS:
        raise RuntimeError("SENDER_POSTAL_ADDRESS is required by CAN-SPAM; set it in .env")
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=60) as s:
        s.login(GMAIL_USER, GMAIL_APP_PASSWORD)
        s.send_message(msg)
    return msg["Message-ID"]
