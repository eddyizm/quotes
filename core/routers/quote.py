'''Shared code'''
from sqlalchemy import select
from core.models.quote_models import Quote, Quote_Staging
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
    query = quotes_staging.select().where(quotes_staging.c.added_to_quotes == False).limit(10)
    return await database.fetch_all(query)


async def submit_new_quote(new_quote: Quote_Staging):
    query = quotes_staging.insert().values(
            quote = new_quote.quote,
            author = new_quote.author,
            category = new_quote.category,
            added_by = new_quote.added_by
        )
    return await database.execute(query)
