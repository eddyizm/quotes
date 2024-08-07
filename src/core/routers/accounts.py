from datetime import datetime, timedelta, timezone
import logging

from fastapi import APIRouter, Form, Depends, Request, Response
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from src.core.config import settings
from src.core.models.user_models import User
from src.core.cf_validate import validate

from src.core.security import AuthHandler

logger = logging.getLogger('uvicorn.error')
templates = Jinja2Templates(directory="src/html/templates")
router = APIRouter(prefix='/account')
auth_handler = AuthHandler()


@router.get("/logout/", response_class=HTMLResponse)
async def logout(request: Request, response: Response):
    logger.info('logging out')
    non_quote_response = settings.non_quote_response(request)
    response = templates.TemplateResponse("/account/logout.html", non_quote_response)
    response.delete_cookie(key='Authorization')
    response.delete_cookie(key='is_loggedin')
    return response


@router.get("/", response_class=HTMLResponse)
async def account(response: Response, request: Request, email=Depends(auth_handler.auth_wrapper)):
    non_quote_response = settings.non_quote_response(request, email)
    response = templates.TemplateResponse("/account/index.html", non_quote_response)
    return response


@router.get("/login", response_class=HTMLResponse)
async def login(response: Response, request: Request):
    non_quote_response = settings.non_quote_response(request)
    response = templates.TemplateResponse("/account/login.html", non_quote_response)
    return response


def login_error_template(request: Request):
    response = templates.TemplateResponse(
        "/account/login_error.html",
        {
            "request": request,
            'detail': 'Incorrect Username or Password. Verify your email and password before trying again.',
            'status_code': 404
        })
    response.headers["HX-Push-Url"] = "/account/error"
    return response


def cf_turnstile_check(request):
    cf_turnstile_response = request._form.get('cf-turnstile-response', '')
    real_ip = request.headers.get('X-Forwarded-For', '') or request.headers.get('x-forwarded-for', '')
    if not cf_turnstile_response:
        return login_error_template(request)
    is_valid = validate(cf_turnstile_response, real_ip)
    if not is_valid.success:
        return login_error_template(request)


@router.post("/authenticate")
async def sign_in(
    request: Request,
    response: Response,
    from_email: str = Form(...), password: str = Form(...)
):
    try:
        turnstile = cf_turnstile_check(request)
        if turnstile:
            return turnstile
        user = User(
            email=from_email,
            password=password
        )
        if await auth_handler.authenticate_user(user.email, user.password):
            jwt_token = auth_handler.create_access_token(user.email)
            non_quote_response = settings.non_quote_response(request)
            non_quote_response['email'] = user.email
            response = templates.TemplateResponse(
                "/account/login_success.html", non_quote_response)
            response.headers["HX-Push-Url"] = "/account/success"
            response.set_cookie(
                key="is_loggedin",
                value=user.email,
                httponly=False,
                expires=datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
            )
            response.set_cookie(key="Authorization", value=f"{jwt_token}", httponly=True)
            return response
        return login_error_template(request)
    except Exception as err:
        logger.exception(f'failure to login: {err}')
        response = templates.TemplateResponse(
            "account/login_error.html",
            {
                "request": request,
                'detail': 'Incorrect Username or Password. Please contact support',
                'status_code': 401
            })
        response.headers["HX-Push-Url"] = "/account/error"
        return response
