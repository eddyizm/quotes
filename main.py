from fastapi import FastAPI

from core.routers import html, quotes_api

app = FastAPI()

app.include_router(html.router)
app.include_router(quotes_api.router)
