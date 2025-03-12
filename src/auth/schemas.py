from pydantic import BaseModel,Field
import uuid
from datetime import datetime
class UserCreateModel(BaseModel):
    username:str=Field(max_length=15)
    email:str=Field(max_length=40)
    password:str=Field(min_length=6)
    first_name:str
    last_name:str

class UserModel(BaseModel):
    uid: uuid.UUID
    username:str
    email:str
    password:str=Field(exclude=True)
    first_name:str
    last_name:str
    created_at:datetime
    updated_at:datetime
    is_verified:bool
