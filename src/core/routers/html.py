from fastapi import APIRouter, Depends, HTTPException, Request, status, Response
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from src.core.config import settings
from src.core.routers.quote import daily_quote, get_random_quote, get_quote_submissions
from src.core.security import AuthHandler


templates = Jinja2Templates(directory="src/html/templates")
router = APIRouter()
auth_handler = AuthHandler()


@router.get("/" ,response_class=HTMLResponse,  status_code=status.HTTP_200_OK)
async def home(response: Response, request:Request): 
    response = templates.TemplateResponse("temp.html", {"request": request, "site_title": settings.SITE_TITLE })
    return response


@router.get("/home" ,response_class=HTMLResponse,  status_code=status.HTTP_200_OK)
async def nav(response: Response, request:Request):
    quote = await daily_quote()
    quote_response = settings.quote_response(request, quote)
    response = templates.TemplateResponse("home.html", 
                                          quote_response)
    return response


@router.get("/random" ,response_class=HTMLResponse,  status_code=status.HTTP_200_OK)
async def random(response: Response, request:Request):
    quote = await get_random_quote()
    quote_response = settings.quote_response(request, quote)
    quote_response['page_title'] = 'Random Quote!'
    response = templates.TemplateResponse("home.html", 
                                          quote_response)
    return response


@router.get("/about" ,response_class=HTMLResponse,  status_code=status.HTTP_200_OK)
async def about(response: Response, request:Request):
    non_quote_response = settings.non_quote_response(request)
    response = templates.TemplateResponse("about.html", 
                                          non_quote_response)
    return response


@router.get("/documentation", response_class=HTMLResponse,  status_code=status.HTTP_200_OK)
async def documentation(response: Response, request:Request):
    non_quote_response = settings.non_quote_response(request)
    response = templates.TemplateResponse("documentation.html", 
                                          non_quote_response)
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
