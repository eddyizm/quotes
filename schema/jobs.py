import asyncio
from datetime import datetime
from dal import database, quote_history
from sql_views import RANDOM_QUOTE
from sqlalchemy import insert


def insert_daily_quote():
  '''
  get a random quote and insert to quote history to use as the daily quote.
  can only run once a date as db date is primary key and unique. 
  '''
  try:
    result = asyncio.run(database.fetch_one(RANDOM_QUOTE))
    query = (
      insert(quote_history).
      values(date_sent=datetime.now().date(), quote_id_fk=result[2])
    )
    asyncio.run(database.execute(query))
  except Exception as ex:
    print('insert failed', ex.with_traceback())