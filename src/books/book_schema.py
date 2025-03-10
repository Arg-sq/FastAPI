from pydantic import BaseModel
from datetime import datetime
import uuid
class Book(BaseModel):
    uid: uuid.UUID
    title: str
    author: str
    year: int
    genre: str
    pages: int
    created_at:datetime
    update_at:datetime

class BookCreateModel(BaseModel):
    title: str
    author: str
    year: int
    genre: str
    pages: int
class UpdateBook(BaseModel):
    title: str
    author: str
    year: int
    genre: str
    pages: int
