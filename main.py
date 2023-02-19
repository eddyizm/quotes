from fastapi import FastAPI

from models.quote_models import Quote
from schema import users, quotes, quote_history, database
from sqlalchemy import select, func

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World!"}


@app.get('/random/', response_model=Quote)
async def random_quote():
    ''' Get random quote '''
    query = 'select quote, author, id from randomQview;'
    return await database.fetch_one(query)

@app.get('/daily/', response_model=Quote)
async def daily_quote():
    ''' Get daily quote '''
    query = select(quotes, quote_history.c.date_sent).join(
        quote_history, quotes.c.id == quote_history.c.quote_id_fk
        ).order_by(quote_history.c.date_sent.desc())
    return await database.fetch_one(query)