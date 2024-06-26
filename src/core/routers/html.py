import logging

from fastapi import APIRouter, Depends, HTTPException, Request, status, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from src.core.config import settings
from src.core.routers.quote import (
    daily_quote,
    get_random_quote,
    get_quote_submissions,
    get_quote_by_id
)
from src.core.security import AuthHandler

logger = logging.getLogger('uvicorn.error')
templates = Jinja2Templates(directory="src/html/templates")
router = APIRouter()
auth_handler = AuthHandler()


@router.get("/404", response_class=HTMLResponse)
async def lost(response: Response, request: Request):
    non_quote_response = settings.non_quote_response(request)
    response = templates.TemplateResponse("404.html", non_quote_response)
    return response


@router.get("/", response_class=HTMLResponse, status_code=status.HTTP_200_OK)
async def home(response: Response, request: Request):
    response = templates.TemplateResponse("temp.html", {"request": request, "site_title": settings.SITE_TITLE})
    return response


@router.get("/home", response_class=HTMLResponse, status_code=status.HTTP_200_OK)
async def nav(response: Response, request: Request):
    quote = await daily_quote()
    quote_response = settings.quote_response(request, quote)
    response = templates.TemplateResponse("home.html", quote_response)
    return response


@router.get("/random", response_class=HTMLResponse, status_code=status.HTTP_200_OK)
async def random(response: Response, request: Request):
    quote = await get_random_quote()
    quote_response = settings.quote_response(request, quote)
    quote_response['page_title'] = 'Random Quote!'
    response = templates.TemplateResponse("home.html", quote_response)
    return response


@router.get("/quote/{id}", response_class=HTMLResponse, status_code=status.HTTP_200_OK)
async def quote_by_id(response: Response, id, request: Request):
    try:
        _id = int(id)
        quote = await get_quote_by_id(_id)
        if not quote:
            return RedirectResponse('/404')
        quote_response = settings.quote_response(request, quote)
        quote_response['page_title'] = 'This Quote!'
        response = templates.TemplateResponse("home.html", quote_response)
        return response
    except ValueError as ex:
        logger.exception(f'return redirect: {ex}')
        return RedirectResponse('/404')
    except HTTPException as ex:
        logger.debug('http exception')
        raise


@router.get("/about", response_class=HTMLResponse, status_code=status.HTTP_200_OK)
async def about(response: Response, request: Request):
    non_quote_response = settings.non_quote_response(request)
    response = templates.TemplateResponse("about.html", non_quote_response)
    return response


@router.get("/documentation", response_class=HTMLResponse, status_code=status.HTTP_200_OK)
async def documentation(response: Response, request: Request):
    non_quote_response = settings.non_quote_response(request)
    response = templates.TemplateResponse("documentation.html", non_quote_response)
    return response


# @router.get("/submissions" ,response_class=HTMLResponse,  status_code=status.HTTP_200_OK)
# async def new_submissions(response: Response, request:Request, email=Depends(auth_handler.auth_wrapper)):
#     # TODO will require additional permissions.
#     submissions = await get_quote_submissions()
#     response = templates.TemplateResponse('submissions.html', 
#                                           {'request': request,
#                                            'submissions': submissions,
#                                            'page_title': 'New Submissions',
#                                            'site_title': settings.SITE_TITLE
#                                            })
#     return response
