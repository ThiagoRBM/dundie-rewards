import re
import smtplib
from email.mime.text import MIMEText

from dundie.settings import SMTP_HOST, SMTP_PORT, SMTP_TIMEOUT
from dundie.utils.log import get_logger

log = get_logger()

regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
#  "r" é de raw string, tudo é passado como está


def check_valid_email(address):
    """Return True if email is valid"""
    return bool(re.fullmatch(regex, address))


def send_mail(from_, to, subject, text):
    if not isinstance(to, list):  # "guard clause checa se foi passada
        # uma lista
        # raise ValueError("'to' must be a list")
        to = [to]  # transforma o que foi passado em lista
    try:  # vê se é possível conectar
        with smtplib.SMTP(
            host=SMTP_HOST, port=SMTP_PORT, timeout=SMTP_TIMEOUT
        ) as server:
            message = MIMEText(text)
            message["Subject"] = subject
            message["From"] = from_
            message["To"] = ",".join(
                to
            )  # precisa ser passada uma lista checagem
            # feita acima
            server.sendmail(from_, to, message.as_string())
    except Exception:
        log.error("Cannot send email to %s", to)
