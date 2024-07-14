from fastapi import APIRouter, status, HTTPException
from src.core.schema.dal import database, users
from src.core.models.user_models import User

from src.core.security import AuthHandler


router = APIRouter(
    prefix="/api/v1",
)
auth_handler = AuthHandler()


# disabled the login and register routes until they are ready to test
# @router.post('/auth/register', status_code=status.HTTP_201_CREATED)
async def register(user: User):
    query = users.insert().values(email = user.email,
        password= auth_handler.get_hash_password(user.password))
    result = await database.execute(query)
    return {'message': result}


@router.post('/auth/login')
async def login(user: User):
    if await auth_handler.authenticate_user(user.email, user.password):
        access_token = auth_handler.create_access_token(user.email)
        print('new token generated and sending response')
        return {'token': access_token}
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail='Username or password incorrect, have you validated your email yet?')
