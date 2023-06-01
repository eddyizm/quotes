from datetime import datetime
import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)
year = datetime.now().year

class Settings:
    SITE_TITLE = os.getenv('SITE_TITLE')
    VERSION = os.getenv('VERSION')
    SECRET_KEY = os.getenv('SECRET_KEY')
    ALGORITHM = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES')
    YEAR=year

    def quote_response(self, request, quote) -> dict:
        return {"request": request, 
        "site_title": settings.SITE_TITLE,
        "year": settings.YEAR,
        "version": settings.VERSION,
        'page_title': 'Daily Quote!',
        "daily_quote": quote }

    def non_quote_response(self, request) -> dict:
        return {"request": request, 
            "site_title": settings.SITE_TITLE,
            "year": settings.YEAR,
            "version": settings.VERSION
            }


settings = Settings()
