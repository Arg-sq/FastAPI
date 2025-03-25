from fastapi.security import HTTPBearer
from fastapi.exceptions import HTTPException
from fastapi.security.http import HTTPAuthorizationCredentials
from fastapi import status ,Request,Depends
from .utils import decode_token
from src.db.redis import token_in_blockList
from src.db.main import  get_Session
from sqlmodel.ext.asyncio.session import AsyncSession
from .service import AuthService
from typing import List
from .models import User

user_service=AuthService()

class TokenBearer(HTTPBearer):
    def  __init__(self,auto_error=True):
        super().__init__(auto_error=auto_error)
        # super le Httpbearer vanne  (parent)class ko init method call gareraxa

    async def __call__(self, request:Request)->HTTPAuthorizationCredentials|None:
        try:
             
            creds= await super().__call__(request)

            token =creds.credentials
    
            token_data=decode_token(token)
            if not self.token_valid(token):
                  raise HTTPException(status_code= status.HTTP_403_FORBIDDEN,detail={
                     "error": "Token is expired or invalid",
                     "resolution":"Please get a new access token"
                })

            if await token_in_blockList(token_data['jti']):
                raise HTTPException(status_code= status.HTTP_403_FORBIDDEN,detail={
                     "error": "Token is blocked or invalid",
                     "resolution":"Please get a new access token"
                })


            self.verify_token_data(token_data)
            return token_data
        
        except Exception as e:
            print(f"❌ Error in TokenBearer: {e}")  # Debugging print
            raise HTTPException(status_code=500, detail=str(e))
    
    def token_valid(self,token:str)->bool:
        token_data=decode_token(token)

        if token_data is not None:
            return True
        else:
            return False
    
    def verify_token_data(self,token_data):
         raise NotImplementedError("Please Override this method in child classes")
        #it raises NotImplementedError) in the parent class.
        # This forces subclasses (AccessTokenBearer and RefreshTokenBearer) to override it.
        # Without overriding, the code would throw an error if an object of TokenBearer were created.  

class AccessTokenBearer(TokenBearer):
        def verify_token_data(self,token_data:dict)->None:
            if token_data and token_data['refresh']:
                raise HTTPException(status.HTTP_403_FORBIDDEN,detail="Please provide Access token")


class RefreshTokenBearer(TokenBearer):
        def verify_token_data(self,token_data:dict)->None:
            if token_data and not token_data['refresh']:
                raise HTTPException(status.HTTP_403_FORBIDDEN,detail="Please provide Refresh token")

async def get_current_user(token_data:dict=Depends(AccessTokenBearer()),session:AsyncSession=Depends(get_Session)):
     user_email=token_data['user']['email']
   
     user=await user_service.get_user_by_email(user_email,session)

     return user

class RoleChecker:
     def __init__(self,allowed_roles:List[str]):
        #   Instance Attributes vs. Local Variables
        #  self.color = color   ✅ Instance Attribute
        # color = "red"        ❌ Local Variable (does NOT affect the instance)
          self.allowed_roles=allowed_roles

     def __call__(self, current_user:User=Depends(get_current_user)):
          
        #   able to access the allowed_roles attribute because it is an instance attribute of the class.
          if current_user.role in self.allowed_roles:
               return True
          raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Operation not permitted for this login cred")
          