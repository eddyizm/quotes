'''Shared code'''
from datetime import datetime
from sqlalchemy import select, exc
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
    query = quotes_staging.select().where(quotes_staging.c.added_to_quotes == False).limit(25)
    return await database.fetch_all(query)


async def submit_new_quote(new_quote: Quote_Staging):
    query = quotes_staging.insert().values(
            quote = new_quote.quote,
            author = new_quote.author,
            category = new_quote.category,
            added_by = new_quote.added_by
        )
    return await database.execute(query)


async def get_submitted_quote_by_id(quote_id) -> Quote:
    """ Get submitted quote from staging table that has not yet been approved"""
    try:
        query = quotes_staging.select().where(quotes_staging.c.added_to_quotes == 0).\
        where(quotes_staging.c.id == quote_id)
        return await database.fetch_one(query)
    except exc.NoResultFound as ex:
        raise ex


async def approve_new_quote(quote_id: int):
    new_quote = get_submitted_quote_by_id(quote_id)
    insert_query =  quotes.insert().values(
            quote = new_quote.quote,
            author = new_quote.author,
            category = new_quote.category,
            date_added = datetime.now().date()
        )
    response = await database.execute(insert_query)
    if response:
        # update original staging quote with new id
        # need to test and validate response is an int and
        # check what an error looks like. Also refactor all of this into smaller functions.
        update_stmt = quotes_staging.update().\
            where(quotes_staging.c.id == quote_id).values(added_to_quotes=response)
        await database.execute(update_stmt)
  
