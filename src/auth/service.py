from .models import User
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from .schemas import UserCreateModel
from .utils import generate_password_hash,decode_token
from fastapi.exceptions import HTTPException
from fastapi import status

class AuthService:
    async def get_user_by_email(self,email:str,session:AsyncSession):
        statement= select(User).where(User.email==email)
        result=await session.exec(statement)
        
        user=result.first()
        return user
        
    async def user_exists(self,email,session:AsyncSession):
        user=await self.get_user_by_email(email,session)
       
        return True if user is not None else False
    

    async def create_user(self,user_payload:UserCreateModel,session:AsyncSession):
        user_payload_dict=user_payload.model_dump()

        new_user =User(**user_payload_dict)
        new_user.password=generate_password_hash(user_payload_dict['password'])
        session.add(new_user)
        await session.commit()
        return new_user
