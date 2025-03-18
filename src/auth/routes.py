from fastapi import APIRouter,Depends,status
from fastapi.exceptions import HTTPException
from .schemas import UserCreateModel,UserModel,LoginModel
from .service import AuthService
from src.db.main import get_Session
from sqlmodel.ext.asyncio.session import AsyncSession
from .utils import create_access_token,verify_password
from datetime import timedelta
from fastapi.responses import JSONResponse


auth_router=APIRouter()
auth_service=AuthService()

REFRESH_TOKEN_EXPIRY=2

@auth_router.post('/signup',response_model=UserModel,status_code=status.HTTP_201_CREATED)
async def create_user(user_payload:UserCreateModel,session:AsyncSession=Depends(get_Session))->dict:
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
      
@auth_router.post("/login")
async def login_user(login_payload:LoginModel,session:AsyncSession=Depends(get_Session)):
    email = login_payload.email
    password = login_payload.password
    print("login done1------------------------")

    user = await auth_service.get_user_by_email(email, session)
    print("login done2------------------------",user)

    if user is not None:
        password_valid = verify_password(password, user.password)
        print("login done3------------------------")

        if password_valid:
            access_token = create_access_token(
                user_data={
                    "email": user.email,
                    "user_uid": str(user.uid),
                    # "role": user.role,
                }
            )

            refresh_token = create_access_token(
                user_data={"email": user.email, "user_uid": str(user.uid)},
                refresh=True,
                expiry=(timedelta(days=REFRESH_TOKEN_EXPIRY)),
            )
            print("login done------------------------")
            return JSONResponse(
                content={
                    "message": "Login successful",
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "user": {"email": user.email, "uid": str(user.uid)},
                }
            )

    raise HTTPException(status.HTTP_404_NOT_FOUND,detail="login invalid")
