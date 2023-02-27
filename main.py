from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from core.routers import html, quotes_api

app = FastAPI()
app.mount("/html/static", StaticFiles(directory="html/static"), name="static")

app.include_router(html.router)
app.include_router(quotes_api.router)
