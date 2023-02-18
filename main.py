from fastapi import FastAPI

from models.quote_models import Quote
from schema import users, quotes, database

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World!"}


@app.get('/random/', response_model=Quote)
async def get_random_quote():
    query = 'select quote, author, id from randomQview;'
    return await database.fetch_one(query)