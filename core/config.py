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
    ACCESS_TOKEN_EXPIRE_MINUTES=60
    YEAR=year


settings = Settings()
