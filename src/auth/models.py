from sqlmodel import SQLModel,Field,Column
from datetime import datetime
import sqlalchemy.dialects.postgresql as pg
import uuid

class User(SQLModel,table=True):
    __tablename__="users"
    uid: uuid.UUID=Field(
        sa_column=Column(pg.UUID,primary_key=True,nullable=False,default=uuid.uuid4),
    )
    username:str
    email:str
    password:str
    first_name:str
    last_name:str
    created_at:datetime=Field(sa_column=Column(pg.TIMESTAMP,default=datetime.now))
    updated_at:datetime=Field(sa_column=Column(pg.TIMESTAMP,default=datetime.now))
    is_verified:bool=Field(default=False)

    def __repr__(self):
        return f"<User {self.username}>"