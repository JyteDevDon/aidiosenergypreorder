import smtplib
from email.message import EmailMessage
from .config import SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASS, SMTP_FROM, SMTP_TO

def send_email(subject: str, body: str) -> None:
    if not SMTP_HOST or not SMTP_TO:
        # Email not configured; do nothing
        return

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = SMTP_FROM
    msg["To"] = SMTP_TO
    msg.set_content(body)

    # STARTTLS
    with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=30) as server:
        server.ehlo()
        try:
            server.starttls()
            server.ehlo()
        except Exception:
            # Some providers may not support STARTTLS on this port; proceed if they require SSL elsewhere.
            pass

        if SMTP_USER and SMTP_PASS:
            server.login(SMTP_USER, SMTP_PASS)

        server.send_message(msg)
