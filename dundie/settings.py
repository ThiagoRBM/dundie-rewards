import os

SMTP_HOST = "localhost"
SMTP_PORT = 8025
SMTP_TIMEOUT = 5

EMAIL_FROM = "master@dundie.com"
DATEFMT: str = "%Y/%m/%d %H:%M:%S"

ROOT_PATH = os.path.dirname(__file__)
DATABASE_PATH = os.path.join(ROOT_PATH, "..", "assets", "database.db")

SQL_CONN_STRING = f"sqlite:///{DATABASE_PATH}"
