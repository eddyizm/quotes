from pydantic import BaseModel


class Quote(BaseModel):
    id: int
    quote: str
    author: str


class Category(BaseModel):
    category: str