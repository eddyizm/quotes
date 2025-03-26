from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import logging

from src.core.routers.accounts import router as AccountsRouter
from src.core.routers.authentication import router as AuthenticationRouter
from src.core.routers.html import router as HtmlRouter
from src.core.routers.quotes_api import router as QuotesApiRouter
from src.core.schema import dal
from src.core.security import RequiresLoginException

logger = logging.getLogger('uvicorn.debug')

app = FastAPI()
logger.debug('app starting up...')

app.mount("/html/static", StaticFiles(directory="src/html/static"), name="static")

app.include_router(HtmlRouter)
app.include_router(QuotesApiRouter)
app.include_router(AuthenticationRouter)
app.include_router(AccountsRouter)

dal.metadata.create_all(dal.engine)


@app.exception_handler(404)
async def not_found_exception_handler(request: Request, exc: HTTPException):
    route_path = request.scope.get('route')
    if route_path and route_path.path.startswith('/api/v1') and \
       request.scope.get('method') == 'POST':
        logger.debug('api 404 error')
        return JSONResponse({"detail": exc.detail}, exc.status_code)
    logger.debug('http request not found')
    return RedirectResponse(url='/404')


'''
 this block is my hack, both in the custom exception handler and middeware to work around jwt token
 handling from the templates.
'''
async def redirect() -> bool:
    raise RequiresLoginException


@app.exception_handler(RequiresLoginException)
async def exception_handler(request: Request, exc: RequiresLoginException):
    return RedirectResponse(url='/account/login')


@app.middleware("http")
async def create_auth_header(request: Request, call_next):
    """
    Check if there are cookies set for authorization. If so, construct the
    Authorization header and modify the request (unless the header already
    exists!)

    # TODO This needs to be updated per the docs ->
        We no longer document this decorator style API, and its usage is discouraged. Instead you should use the following approach:
        >>> middleware = [Middleware(...), ...]
        >>> app = Starlette(middleware=middleware)
    """
    if ("Authorization" not in request.headers and "Authorization" in request.cookies):
        access_token = request.cookies["Authorization"]
        request.headers.__dict__["_list"].append(
            (
                "authorization".encode(),
                f"Bearer {access_token}".encode(),
            )
        )
    elif ("Authorization" not in request.headers and "Authorization" not in request.cookies):
        request.headers.__dict__["_list"].append(
            (
                "authorization".encode(),
                "Bearer 12345".encode(),
            )
        )
    response = await call_next(request)
    return response
# end block

@app.on_event("startup")
async def startup():
    await dal.database.connect()
    logger.debug('database connected on startup')


@app.on_event("shutdown")
async def shutdown():
    await dal.database.disconnect()
