from fastapi import APIRouter, Request, status, Response
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from core.config import settings

templates = Jinja2Templates(directory="html/templates")
router = APIRouter()


@router.get("/" ,response_class=HTMLResponse,  status_code=status.HTTP_200_OK)
async def home(response: Response, request:Request): 
    response = templates.TemplateResponse("base.html", {"request": request, "site_title": settings.SITE_TITLE })
    return response
