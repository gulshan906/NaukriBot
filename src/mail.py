"""
===========================================================
Project : NaukriBot
Module  : mail.py
Author  : Gulshan Singh
Version : 3.0.0
===========================================================
"""

import smtplib
from pathlib import Path

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

from config.config import (
    GMAIL_USER,
    GMAIL_APP_PASSWORD,
    RECIPIENT_EMAIL,
)

from src.logger import logger


# ===========================================================
# Attach File
# ===========================================================

def attach_file(message, file_path):

    try:

        if not file_path:

            return

        file_path = Path(file_path)

        if not file_path.exists():

            logger.warning(
                f"Attachment Not Found : {file_path}"
            )

            return

        with open(file_path, "rb") as file:

            part = MIMEBase(
                "application",
                "octet-stream"
            )

            part.set_payload(file.read())

        encoders.encode_base64(part)

        part.add_header(

            "Content-Disposition",

            f'attachment; filename="{file_path.name}"'

        )

        message.attach(part)

        logger.info(
            f"Attachment Added : {file_path.name}"
        )

    except Exception as e:

        logger.exception(e)


# ===========================================================
# Send Email
# ===========================================================

def send_email(

    subject: str,

    body: str,

    attachment=None,

):

    try:

        message = MIMEMultipart()

        message["From"] = GMAIL_USER

        message["To"] = RECIPIENT_EMAIL

        message["Subject"] = subject

        # ------------------------------------------
        # Plain Text
        # ------------------------------------------

        message.attach(

            MIMEText(

                body,

                "plain",

                "utf-8"

            )

        )

        # ------------------------------------------
        # Attachment
        # ------------------------------------------

        if attachment:

            if isinstance(

                attachment,

                (list, tuple)

            ):

                for file in attachment:

                    attach_file(

                        message,

                        file

                    )

            else:

                attach_file(

                    message,

                    attachment

                )

        # ------------------------------------------
        # Gmail SMTP
        # ------------------------------------------

        server = smtplib.SMTP(

            "smtp.gmail.com",

            587

        )

        server.starttls()

        server.login(

            GMAIL_USER,

            GMAIL_APP_PASSWORD,

        )

        server.sendmail(

            GMAIL_USER,

            RECIPIENT_EMAIL,

            message.as_string(),

        )

        server.quit()

        logger.info(

            "Email Sent Successfully."

        )

        return True

    except Exception as e:

        logger.exception(e)

        return False