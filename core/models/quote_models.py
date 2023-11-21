from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Quote(BaseModel):
    id: int
    quote: str
    author: str
    category: str


class Category(BaseModel):
    category: str


class Author(BaseModel):
    author: str


class Quote_Staging(BaseModel):
    id: Optional[int]
    quote: str
    author: str
    category: str
    added_to_quotes: Optional[bool]
    added_by: str
