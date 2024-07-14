import logging

from fastapi import APIRouter, Cookie, Form, Depends, HTTPException, Request, status, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from src.core.config import settings
from src.core.cf_validate import validate
from src.core.models.user_models import Message
from src.core.schema.jobs import send_message
from src.core.routers.quote import (
    daily_quote,
    get_random_quote,
    get_quote_submissions,
    get_quote_by_id
)
from src.core.security import AuthHandler
from typing import Optional

logger = logging.getLogger('uvicorn.error')
templates = Jinja2Templates(directory="src/html/templates")
router = APIRouter()
auth_handler = AuthHandler()


@router.get("/404", response_class=HTMLResponse)
async def lost(response: Response, request: Request, is_loggedin: Optional[str] = Cookie(None)):
    non_quote_response = settings.non_quote_response(request, is_loggedin)
    response = templates.TemplateResponse("404.html", non_quote_response)
    return response


@router.get("/", response_class=HTMLResponse)
async def nav(response: Response, request: Request, is_loggedin: Optional[str] = Cookie(None)):
    quote = await daily_quote()
    quote_response = settings.quote_response(request, quote, user_email=is_loggedin)
    response = templates.TemplateResponse("home.html", quote_response)
    response.headers["Cache-Control"] = "public, max-age=21600"
    return response


@router.get("/random", response_class=HTMLResponse)
async def random(response: Response, request: Request, is_loggedin: Optional[str] = Cookie(None)):
    quote = await get_random_quote()
    quote_response = settings.quote_response(request, quote, user_email=is_loggedin)
    quote_response['page_title'] = 'Random Quote!'
    response = templates.TemplateResponse("home.html", quote_response)
    return response


@router.get("/quote/{id}", response_class=HTMLResponse)
async def quote_by_id(response: Response, id, request: Request, is_loggedin: Optional[str] = Cookie(None)):
    try:
        _id = int(id)
        quote = await get_quote_by_id(_id)
        if not quote:
            return RedirectResponse('/404')
        quote_response = settings.quote_response(request, quote, user_email=is_loggedin)
        quote_response['page_title'] = 'This Quote!'
        response = templates.TemplateResponse("home.html", quote_response)
        response.headers["Cache-Control"] = "public, max-age=604800"
        return response
    except ValueError as ex:
        logger.exception(f'return redirect: {ex}')
        return RedirectResponse('/404')
    except HTTPException as ex:
        logger.debug('http exception')
        raise


@router.get("/about", response_class=HTMLResponse, status_code=status.HTTP_200_OK)
async def about(response: Response, request: Request, is_loggedin: Optional[str] = Cookie(None)):
    non_quote_response = settings.non_quote_response(request, is_loggedin)
    response = templates.TemplateResponse("about.html", non_quote_response)
    response.headers["Cache-Control"] = "public, max-age=21600"
    return response


@router.post("/hello", response_class=HTMLResponse)
def hello(
        response: Response,
        request: Request,
        message: str = Form(...),
        from_email: str = Form(...),
        is_loggedin: Optional[str] = Cookie(None)):
    cf_turnstile_response = request._form.get('cf-turnstile-response', '')
    non_quote_response = settings.non_quote_response(request, is_loggedin)
    real_ip = request.headers.get('X-Forwarded-For', '') or request.headers.get('x-forwarded-for', '')
    logger.info(f'getting ip from headers: {real_ip}')
    response = templates.TemplateResponse("email_failure.html", non_quote_response)
    if not cf_turnstile_response:
        return response
    is_valid = validate(cf_turnstile_response, real_ip)  # TODO need an ip here
    if not is_valid.success:
        return response
    if send_message(
        Message(
            from_email=from_email,
            message=message,
            submission_ip=real_ip
        )
    ) == 200:
        response = templates.TemplateResponse("email_success.html", non_quote_response)
    return response


@router.get("/documentation", response_class=HTMLResponse, status_code=status.HTTP_200_OK)
async def documentation(response: Response, request: Request, is_loggedin: Optional[str] = Cookie(None)):
    non_quote_response = settings.non_quote_response(request, is_loggedin)
    response = templates.TemplateResponse("documentation.html", non_quote_response)
    return response


@router.get("/submissions", response_class=HTMLResponse)
async def new_submissions(response: Response, request: Request, email=Depends(auth_handler.auth_wrapper)):
    # TODO will require additional permissions.
    submissions = await get_quote_submissions()
    non_quote_response = settings.non_quote_response(request, user_email=email)
    non_quote_response['page_title'] = 'New Submissions'
    non_quote_response['submissions'] = submissions
    response = templates.TemplateResponse('submissions.html', non_quote_response)
    return response
