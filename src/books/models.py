from sqlmodel import SQLModel,Field,Column
from datetime import datetime,date
import uuid

import sqlalchemy.dialects.postgresql as pg

# In PostgreSQL, UUIDs have a dedicated data type (UUID).
# SQLAlchemy’s default String type does not automatically map to UUID in PostgreSQL.
# Using pg.UUID ensures the database stores the UUID as a real UUID type, not just a string.
# 
class Book(SQLModel,table=True):
    __tablename__="fastBooks"
    uid: uuid.UUID=Field(
        sa_column=Column(pg.UUID,primary_key=True,nullable=False,default=uuid.uuid4),
    )
    title: str
    author: str
    year: int
    genre: str
    pages: int
    published_date:date
    created_at:datetime=Field(sa_column=Column(pg.TIMESTAMP,default=datetime.now))
    updated_at:datetime=Field(sa_column=Column(pg.TIMESTAMP,default=datetime.now))

def __repr__(self):
    return f"<Book {self.title}>"