import logging

from fastapi import APIRouter, Form, Depends, HTTPException, Request, status, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from src.core.config import settings
from src.core.cf_validate import validate

from src.core.security import AuthHandler

logger = logging.getLogger('uvicorn.error')
templates = Jinja2Templates(directory="src/html/templates")
router = APIRouter(prefix='/accounts')
# auth_handler = AuthHandler()


@router.get("/login", response_class=HTMLResponse)
async def login(response: Response, request: Request):
    non_quote_response = settings.non_quote_response(request)
    response = templates.TemplateResponse("/accounts/login.html", non_quote_response)
    return response
