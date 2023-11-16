from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from core.routers import authentication, html, quotes_api
from core.schema import dal

app = FastAPI()
app.mount("/html/static", StaticFiles(directory="html/static"), name="static")

app.include_router(html.router)
app.include_router(quotes_api.router)
app.include_router(authentication.router)

dal.metadata.create_all(dal.engine)

@app.on_event("startup")
async def startup():
    await dal.database.connect()


@app.on_event("shutdown")
async def shutdown():
    await dal.database.disconnect()
