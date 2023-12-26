from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi import Security
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Any, Union
from jose import jwt
from src.core.config import settings


class AuthHandler():
    security = HTTPBearer()
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    ALGORITHM = settings.ALGORITHM


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


    def create_access_token(self,
        subject: Union[str, Any], expires_delta: timedelta = None
    ) -> str:
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(
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