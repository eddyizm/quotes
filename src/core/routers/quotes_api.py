import logging

from fastapi import APIRouter, Depends, HTTPException, Response
from typing import List
from sqlalchemy import select

from src.core.models.quote_models import Author, Category, Quote, Quote_Staging
from src.core.routers.quote import (
    daily_quote,
    get_random_quote,
    get_quote_submissions,
    submit_new_quote,
    approve_new_quote,
    reject_new_quote,
    get_quote_by_id
)
from src.core.security import AuthHandler
from src.core.schema.dal import quotes, database

logger = logging.getLogger('uvicorn.error')
router = APIRouter(
    prefix="/api/v1",
)
auth_handler = AuthHandler()


@router.post('/random/', response_model=Quote)
async def random_quote():
    ''' Get random quote '''
    return await get_random_quote()


@router.post('/daily/', response_model=Quote)
async def get_daily_quote():
    ''' Get daily quote '''
    return await daily_quote()


@router.post('/quote/{id}', response_model=Quote)
async def quote_by_id_perma(id: int):
    ''' Get daily quote '''
    response = await get_quote_by_id(id)
    if not response:
        raise HTTPException(status_code=404, detail='Quote not found')
    return response


@router.post('/categories/', response_model=List[Category])
async def categories(email=Depends(auth_handler.auth_wrapper)):
    ''' return list of categories '''
    query = select([quotes.c.category]).distinct().order_by(quotes.c.category)
    return await database.fetch_all(query)


@router.post('/authors/', response_model=List[Author])
async def authors(email=Depends(auth_handler.auth_wrapper)):
    ''' return list of authors '''
    query = select([quotes.c.author]).distinct().order_by(quotes.c.author)
    return await database.fetch_all(query)


@router.post('/quote/submit/')
async def new_quote(new_quote: Quote_Staging, email=Depends(auth_handler.auth_wrapper)):
    ''' new quote submission '''
    try:
        # TODO make this a form submission endpoint.
        return await submit_new_quote(new_quote)
    except HTTPException:
        raise HTTPException


@router.post('/quote/submissions/', response_model=List[Quote_Staging])
async def submissions(email=Depends(auth_handler.auth_wrapper)):
    ''' Return list of unprocess quote submissions '''
    # TODO this will be an elevated permission
    try:
        return await get_quote_submissions()
    except HTTPException:
        raise HTTPException


@router.patch('/quote/submissions/{id}')
async def approve_submission(id: int, email=Depends(auth_handler.auth_wrapper)):
    ''' Approve a quote submission by id '''
    # TODO this will be an elevated permission
    try:
        result = await approve_new_quote(id)
        if result is None:
            return Response()
    except HTTPException:
        raise HTTPException


@router.patch('/quote/submissions/reject/{id}')
async def reject_submission(id: int, email=Depends(auth_handler.auth_wrapper)):
    ''' Reject a quote submission by id (soft delete)'''
    # TODO this will be an elevated permission
    try:
        result = await reject_new_quote(id)
        if result is None:
            return Response()
    except HTTPException:
        raise HTTPException

