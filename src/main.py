from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import logging

from src.core.routers import authentication, html, quotes_api
from src.core.schema import dal

logger = logging.getLogger('uvicorn.error')

app = FastAPI()
logger.debug('app starting up...')

app.mount("/html/static", StaticFiles(directory="src/html/static"), name="static")

app.include_router(html.router)
app.include_router(quotes_api.router)
app.include_router(authentication.router)

dal.metadata.create_all(dal.engine)

@app.on_event("startup")
async def startup():
    await dal.database.connect()
    logger.debug('database connected on startup')


@app.on_event("shutdown")
async def shutdown():
    await dal.database.disconnect()
