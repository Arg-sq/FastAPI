from fastapi import APIRouter,Depends,status
from fastapi.exceptions import HTTPException
from .schemas import UserCreateModel,UserModel
from .service import AuthService
from src.db.main import get_Session
from sqlmodel.ext.asyncio.session import AsyncSession

auth_router=APIRouter()
auth_service=AuthService()

@auth_router.post('/signup',response_model=UserModel,status_code=status.HTTP_201_CREATED)
async def crete_user(user_payload:UserCreateModel,session:AsyncSession=Depends(get_Session))->dict:
   user_email=user_payload.email
   user_exist =await auth_service.get_user_by_email(user_email,session)
 
   if user_exist:
      raise HTTPException(status.HTTP_403_FORBIDDEN,detail="User with email already exists")
   else:
         new_user= await auth_service.create_user(user_payload,session)
         if new_user is not None:
             return new_user
         else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Something went wrong")
      
