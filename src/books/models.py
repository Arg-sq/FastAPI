from sqlmodel import SQLModel,Field,Column
from datetime import datetime
import uuid

import sqlalchemy.dialects.postgresql as pg

class Book(SQLModel,table=True):
    __tablename__="fastBooks"
    uid: uuid.UUID=Field(
        sa_column=Column(pg.UUID,primary_key=True,nullable=False,default=uuid.uuid4()),
    )
    title: str
    author: str
    year: int
    genre: str
    pages: int
    created_at:datetime=Field(sa_column=Column(pg.TIMESTAMP,default=datetime.now))
    updated_at:datetime=Field(sa_column=Column(pg.TIMESTAMP,default=datetime.now))

def __repr__(self):
    return f"<Book {self.title}>"