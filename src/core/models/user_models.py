from pydantic import BaseModel, EmailStr


class User(BaseModel):
    email: EmailStr
    password: str


class Message(BaseModel):
    from_email: EmailStr
    message: str
