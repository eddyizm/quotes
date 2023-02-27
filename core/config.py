import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

class Settings:
    SITE_TITLE = os.getenv('SITE_TITLE')


settings = Settings()
