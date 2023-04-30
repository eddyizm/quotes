'''Shared code'''
from sqlalchemy import select
from core.models.quote_models import Quote
from core.schema.sql_views import RANDOM_QUOTE
from core.schema.dal import quotes, quote_history, quotes_staging, database


async def daily_quote() -> Quote:
    ''' Get daily quote '''
    query = select(quotes, quote_history.c.date_sent).join(
        quote_history, quotes.c.id == quote_history.c.quote_id_fk
        ).order_by(quote_history.c.date_sent.desc())
    return await database.fetch_one(query)


async def get_random_quote():
    return await database.fetch_one(RANDOM_QUOTE)


async def get_quote_submissions():
    query = quotes_staging.select()
    return await database.fetch_all(query)
