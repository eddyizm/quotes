from datetime import datetime
import os
from dotenv import load_dotenv
from urllib.parse import quote

dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path)
year = datetime.now().year


class Settings:
    SITE_TITLE = os.getenv("SITE_TITLE")
    VERSION = os.getenv("VERSION")
    SECRET_KEY = os.getenv("SECRET_KEY")
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
    YEAR = year
    POSTGRES_SERVER = os.getenv("POSTGRES_SERVER")
    POSTGRES_USER = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = quote(os.getenv("POSTGRES_PASSWORD"))
    POSTGRES_DB = os.getenv("POSTGRES_DB")
    POSTGRES_PORT = os.getenv("POSTGRES_PORT")
    MAILGUN_KEY = os.getenv("MAILGUN_KEY")
    MAILGUN_URL = os.getenv("MAILGUN_URL")
    POSTMASTER_EMAIL = os.getenv("POSTMASTER_EMAIL")

    def quote_response(self, request, quote) -> dict:
        return {
            "request": request,
            "site_title": self.SITE_TITLE,
            "year": self.YEAR,
            "version": self.VERSION,
            "page_title": "Daily Quote!",
            "daily_quote": quote,
        }

    def non_quote_response(self, request) -> dict:
        return {
            "request": request,
            "site_title": self.SITE_TITLE,
            "year": self.YEAR,
            "version": self.VERSION,
        }


settings = Settings()
