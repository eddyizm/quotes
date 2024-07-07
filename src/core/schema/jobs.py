from datetime import datetime

from fastapi import HTTPException
import requests
from sqlalchemy import insert

from .dal import database, quote_history
from .sql_views import RANDOM_QUOTE
from src.core.config import settings
from src.core.models.user_models import Message

async def insert_daily_quote():
    '''
    get a random quote and insert to quote history to use as the daily quote.
    can only run once a date as db date is primary key and unique.
    '''
    try:
        print('Getting random quote for daily insert')
        result = await database.fetch_one(RANDOM_QUOTE)
        query = (
            insert(quote_history).
            values(date_sent=datetime.now().date(), quote_id_fk=result[2])
        )
        print('inserting to history table')
        await database.execute(query)
        print(f'daily quote successfully inserted {result[2]}')
    except Exception as ex:
        print('insert failed', ex)


def send_message(message: Message):
    body = "\n".join(message.dict().values())
    try:
        response = requests.post(
            settings.MAILGUN_URL,
            auth=("api", settings.MAILGUN_KEY),
            data={
                "from": settings.POSTMASTER_EMAIL,
                "to": 'noone@ragingdharma.com',
                "subject": "RagingDharma Website Inquiry",
                "text": body
            })
        return response.status_code
    except HTTPException:
        raise HTTPException(status_code=response.status_code, detail='problem sending message')
