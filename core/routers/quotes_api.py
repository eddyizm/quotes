from fastapi import APIRouter
from core.models.quote_models import Author, Category, Quote 
from core.schema.dal import quotes, quote_history, database
from core.schema.sql_views import RANDOM_QUOTE
from typing import List
from sqlalchemy import select

router = APIRouter(
        prefix="/api/v1",
    )

async def get_random_quote():
    return await database.fetch_one(RANDOM_QUOTE)

@router.post('/random/', response_model=Quote)
async def random_quote():
    ''' Get random quote '''
    return await get_random_quote()    


@router.post('/daily/', response_model=Quote)
async def daily_quote():
    ''' Get daily quote '''
    query = select(quotes, quote_history.c.date_sent).join(
        quote_history, quotes.c.id == quote_history.c.quote_id_fk
        ).order_by(quote_history.c.date_sent.desc())
    return await database.fetch_one(query)


@router.post('/categories/', response_model=List[Category])
async def categories():
    ''' return list of categories '''
    query = select([quotes.c.category]).distinct().order_by(quotes.c.category)
    return await database.fetch_all(query)


@router.post('/authors/', response_model=List[Author])
async def authors():
    ''' return list of categories '''
    query = select([quotes.c.author]).distinct().order_by(quotes.c.author)
    return await database.fetch_all(query)
