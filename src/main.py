from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import RedirectResponse, JSONResponse
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


@app.exception_handler(404)
async def not_found_exception_handler(request: Request, exc: HTTPException):
    route_path = request.scope.get('route')
    if route_path and route_path.startswith('/api/v1') and \
       request.cope.get('method') == 'POST':
        logger.debug('api 404 error')
        return JSONResponse({"detail": exc.detail}, exc.status_code)
    logger.debug('http request not found')
    return RedirectResponse(url='/404')


@app.on_event("startup")
async def startup():
    await dal.database.connect()
    logger.debug('database connected on startup')


@app.on_event("shutdown")
async def shutdown():
    await dal.database.disconnect()
