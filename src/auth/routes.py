from fastapi import APIRouter,Depends,status
from fastapi.exceptions import HTTPException
from .schemas import UserCreateModel,UserModel,LoginModel
from .service import AuthService
from src.db.main import get_Session
from sqlmodel.ext.asyncio.session import AsyncSession
from .utils import create_access_token,verify_password
from datetime import timedelta,datetime
from fastapi.responses import JSONResponse
from .dependencies import RefreshTokenBearer,AccessTokenBearer,get_current_user,RoleChecker
from src.db.redis import add_jti_to_block

auth_router=APIRouter()
auth_service=AuthService()
role_checker=RoleChecker(["admin","user"])

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

    user = await auth_service.get_user_by_email(email, session)
  

    if user is not None:
        password_valid = verify_password(password, user.password)
      

        if password_valid:
            access_token = create_access_token(
                user_data={
                    "email": user.email,
                    "user_uid": str(user.uid),
                    "role": user.role,
                }
            )

            refresh_token = create_access_token(
                user_data={"email": user.email, "user_uid": str(user.uid)},
                refresh=True,
                expiry=(timedelta(days=REFRESH_TOKEN_EXPIRY)),
            )
         
            return JSONResponse(
                content={
                    "message": "Login successful",
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "user": {"email": user.email, "uid": str(user.uid)},
                }
            )

    raise HTTPException(status.HTTP_403_FORBIDDEN,detail="login invalid")

@auth_router.delete("/deleteUser/{user_uid}")
async def delete_user(user_uid: str, session: AsyncSession = Depends(get_Session)):
    pass

@auth_router.get("/new_access_token")
async def get_new_access_token(token_details:dict=Depends(RefreshTokenBearer())):
    expiry_timestamp=token_details['exp']
    print(token_details)

    if datetime.fromtimestamp(expiry_timestamp)>datetime.now():
        new_access_token=create_access_token(
            user_data=token_details['user']
        )
        return JSONResponse(content={
            "access_token":new_access_token
        })
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Invalid or expired token")

@auth_router.get("/profile",response_model=UserModel)
async def get_curent_user(user=Depends(get_current_user),_:bool=Depends(role_checker)):
    return user


@auth_router.get("/logout")
async def handle_revoke_token(token_details:dict=Depends(AccessTokenBearer())):
    jti=token_details['jti']

    await add_jti_to_block(jti)
    return JSONResponse(
        content={
            "message":"Logged out successfully"
        },
        status_code=status.HTTP_200_OK
    )
