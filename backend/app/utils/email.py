import smtplib
from email.message import EmailMessage

import app.core.config as config


def send_email(
    to_email: str,
    subject: str,
    body: str,
):
    print("EMAIL:", config.EMAIL_ADDRESS)
    print("PASSWORD:", config.EMAIL_PASSWORD)

    msg = EmailMessage()

    msg["Subject"] = subject
    msg["From"] = config.EMAIL_ADDRESS
    msg["To"] = to_email

    msg.set_content(body)

    with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
        smtp.starttls()

        smtp.login(
            config.EMAIL_ADDRESS,
            config.EMAIL_PASSWORD,
        )

        smtp.send_message(msg)