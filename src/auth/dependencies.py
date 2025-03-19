from fastapi.security import HTTPBearer
from fastapi.exceptions import HTTPException
from fastapi.security.http import HTTPAuthorizationCredentials
from fastapi import status ,Request
from .utils import decode_token

class TokenBearer(HTTPBearer):
    def  __init__(self,auto_error=True):
        super().__init__(auto_error=auto_error)
        # super le Httpbearer vanne  (parent)class ko init method call gareraxa

    async def __call__(self, request:Request)->HTTPAuthorizationCredentials|None:
        creds= await super().__call__(request)

        token =creds.credentials
  
        token_data=decode_token(token)
        if not self.token_valid(token):
            raise HTTPException(status.HTTP_403_FORBIDDEN,detail="Invalid or expired token")
       
        self.verify_token_data(token_data)
        return token_data

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

