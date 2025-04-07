from sqlmodel import SQLModel,Field,Column,Relationship
from datetime import datetime
import sqlalchemy.dialects.postgresql as pg
import uuid
from typing import List
from src.books import models

class User(SQLModel,table=True):
    __tablename__="users"
    uid: uuid.UUID=Field(
        sa_column=Column(pg.UUID,primary_key=True,nullable=False,default=uuid.uuid4),
    )
    username:str
    email:str
    password:str=Field(exclude=True)
    first_name:str
    last_name:str
    role:str=Field(sa_column=Column(
        pg.VARCHAR,nullable=False,server_default="user"
    ))
    created_at:datetime=Field(sa_column=Column(pg.TIMESTAMP,default=datetime.now))
    updated_at:datetime=Field(sa_column=Column(pg.TIMESTAMP,default=datetime.now))
    is_verified:bool=Field(default=False)
    books:List["models.Book"]=Relationship(back_populates="user",sa_relationship_kwargs={"lazy":"selectin"})

    def __repr__(self):
        return f"<User {self.username}>"