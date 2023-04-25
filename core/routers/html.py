from fastapi import APIRouter, Request, status, Response
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from core.config import settings
from core.routers.quote import daily_quote, get_random_quote

templates = Jinja2Templates(directory="html/templates")
router = APIRouter()


@router.get("/" ,response_class=HTMLResponse,  status_code=status.HTTP_200_OK)
async def home(response: Response, request:Request): 
    response = templates.TemplateResponse("temp.html", {"request": request, "site_title": settings.SITE_TITLE })
    return response


@router.get("/home" ,response_class=HTMLResponse,  status_code=status.HTTP_200_OK)
async def nav(response: Response, request:Request):
    quote = await daily_quote()
    response = templates.TemplateResponse("home.html", 
                                          {"request": request, 
                                           "site_title": settings.SITE_TITLE,
                                           'page_title': 'Daily Quote!',
                                            "daily_quote": quote })
    return response


@router.get("/random" ,response_class=HTMLResponse,  status_code=status.HTTP_200_OK)
async def random(response: Response, request:Request):
    quote = await get_random_quote()
    response = templates.TemplateResponse("home.html", 
                                          {"request": request, 
                                           "site_title": settings.SITE_TITLE,
                                           'page_title': 'Random Quote!',
                                            "daily_quote": quote })
    return response
