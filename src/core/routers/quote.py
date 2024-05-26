'''Shared code'''
from datetime import datetime
from fastapi import Depends
from sqlalchemy import select, exc
from src.core.models.quote_models import Quote, Quote_Staging
from src.core.schema.sql_views import RANDOM_QUOTE
from src.core.schema.dal import quotes, quote_history, quotes_staging, database, connect_to_db
import logging

logger = logging.getLogger('uvicorn.error')

async def daily_quote(db=Depends(connect_to_db)) -> Quote:
    ''' Get daily quote '''
    logger.info('Getting dailyl quote')
    query = select(
        quotes, quote_history.c.date_sent).join(
        quote_history, quotes.c.id == quote_history.c.quote_id_fk
    ).order_by(quote_history.c.date_sent.desc())
    return await database.fetch_one(query)


async def get_random_quote(db=Depends(connect_to_db)):
    return await database.fetch_one(RANDOM_QUOTE)


async def get_quote_submissions(db=Depends(connect_to_db)):
    query = quotes_staging.select().where(quotes_staging.c.added_to_quotes == 0).limit(50)
    return await database.fetch_all(query)


async def submit_new_quote(new_quote: Quote_Staging, db=Depends(connect_to_db)):
    try:
        query = quotes_staging.insert().values(
            quote=new_quote.quote,
            author=new_quote.author,
            category=new_quote.category,
            added_by=new_quote.added_by
        )
        return await database.execute(query)
    except Exception as ex:
        logger.exception(f'exceptiion detail: object \n{new_quote}\n{ex}')


async def update_submitted_quote(quote_id, response, db=Depends(connect_to_db)):
    """ Set added to quote field to new quote id, flagging as updated """
    update_stmt = quotes_staging.update().\
        where(quotes_staging.c.id == quote_id).\
        values(added_to_quotes=response)
    return await database.execute(update_stmt)


async def insert_new_quote(new_quote, db=Depends(connect_to_db)):
    """given new quote, insert to quotes table"""
    logger.info('Inserting new quote')
    insert_query = quotes.insert().values(
        quote=new_quote.quote,
        author=new_quote.author,
        category=new_quote.category,
        date_added=datetime.now().date()
    )
    response = await database.execute(insert_query)
    return response


async def get_submitted_quote_by_id(quote_id, db=Depends(connect_to_db)) -> Quote:
    """ Get submitted quote from staging table that has not yet been approved"""
    try:
        
        query = quotes_staging.select().where(quotes_staging.c.added_to_quotes == 0).\
            where(quotes_staging.c.id == quote_id)
        return await database.fetch_one(query)
    except exc.NoResultFound as ex:
        raise ex


async def approve_new_quote(quote_id: int, db=Depends(connect_to_db)):
    """
        approve submitted quote
        TODO will need to add a fuzzy duplicate check
    """
    new_quote = await get_submitted_quote_by_id(quote_id)
    response = await insert_new_quote(new_quote)
    if response:
        return await update_submitted_quote(quote_id, response)
