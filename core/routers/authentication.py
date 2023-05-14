from fastapi import APIRouter, status, HTTPException
from core.schema.dal import database, users
from core.models.user_models import User

from core.security import AuthHandler, RequiresLoginException


router = APIRouter()
auth_handler = AuthHandler()


async def authenticate_user(username, password):
    try:
        user = User(email = username,
            password= password)  
        
        query = users.select().where((users.c.email == user.email) & (users.c.is_active == True))
        result =  await database.fetch_one(query)
        if result: 
            print('user found, check password')
            password_check = auth_handler.verify_password(user.password, result[2])
            print(f'password check result: {password_check}')
            return password_check
        else: 
            return False
    except:
        raise RequiresLoginException()


@router.post('/auth/register', status_code=status.HTTP_201_CREATED)
async def register(user: User):
    query = users.insert().values(email = user.email,
        password= auth_handler.get_hash_password(user.password))
    result = await database.execute(query)
    return {'message': result}



@router.post('/auth/login')
async def login(user: User):
    if await authenticate_user(user.email, user.password):
        atoken = auth_handler.create_access_token(user.email)
        print('new token generated and sending response')
        return { 'token': atoken }
    else: 
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail='Username or password incorrect, have you validated your email yet?')
