from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi import Security
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from typing import Any, Union
from jose import jwt

from src.core.config import settings
from src.core.models.user_models import User
from src.core.schema.dal import database, users

class AuthHandler():
    security = HTTPBearer()
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    ALGORITHM = settings.ALGORITHM

    async def authenticate_user(self, username, password):
        try:
            user = User(email=username,
                        password=password)
            query = users.select().where((users.c.email == user.email) & (users.c.is_active == True))
            result = await database.fetch_one(query)
            if result:
                print('user found, check password')
                password_check = self.verify_password(user.password, result[2])
                print(f'password check result: {password_check}')
                return password_check
            else:
                return False
        except RequiresLoginException:
            raise RequiresLoginException()

    def decode_token(self, token):
        try:
            print('decoding')
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=settings.ALGORITHM)
            return payload['sub']
        except jwt.ExpiredSignatureError:
            raise RequiresLoginException()
            # raise HTTPException(status_code=401, detail='Signature has expired')
        except jwt.JWTError as e:
            raise RequiresLoginException()
            # raise HTTPException(status_code=401, detail='Invalid token')
        except Exception as e:
            raise RequiresLoginException()

    def auth_wrapper(self, auth: HTTPAuthorizationCredentials = Security(security)):
        return self.decode_token(auth.credentials)

    def create_access_token(
        self,
        subject: Union[str, Any], expires_delta: timedelta = None
    ) -> str:
        if expires_delta:
            expire = datetime.now(timezone.UTC) + expires_delta
        else:
            expire = datetime.now(timezone.UTC) + timedelta(
                minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
            )
        to_encode = {"exp": expire, "sub": str(subject)}
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt

    def get_hash_password(self, plain_password):
        return self.pwd_context.hash(plain_password)

    def verify_password(self, plain_password, hash_password):
        return self.pwd_context.verify(plain_password, hash_password)

    def is_admin(self):
        # TODO -add admin role or scope
        pass


class RequiresLoginException(Exception):
    pass
