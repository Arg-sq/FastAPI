from fastapi import APIRouter,Depends,status
from fastapi.exceptions import HTTPException
from schemas import UserCreateModel
from .service import AuthService
from src.db.main import get_Session
from sqlmodel.ext.asyncio.session import AsyncSession

auth_router=APIRouter()
auth_service=AuthService()

@auth_router.post('/signup')
async def crete_user(user_payload:UserCreateModel,session:AsyncSession=Depends(get_Session))->dict:
   new_user= await auth_service.create_user(user_payload,session)
   if new_user is not None:
      return new_user
   else:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Something went wrong")