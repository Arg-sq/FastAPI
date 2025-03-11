from fastapi import APIRouter,status,Depends
from fastapi.exceptions import HTTPException
from src.books.book_schema import Book,UpdateBook,BookCreateModel
from src.db.main import get_Session
from sqlmodel.ext.asyncio.session import AsyncSession
from src.books.service import BookService
from typing import List

book_router=APIRouter()
book_service=BookService()

@book_router.get('/books',response_model=List[Book])
async def get_all_books(session:AsyncSession=Depends(get_Session))->list:
#     Here, session: AsyncSession = Depends(get_Session) injects a database session into the function.
    books=await book_service.get_all_books(session)
    return books

@book_router.post('/add_books',status_code=status.HTTP_201_CREATED,response_model=Book)
async def create_a_book(book_payload:BookCreateModel,session:AsyncSession=Depends(get_Session))->dict:
    #   FastAPI does NOT pass payload directly as a dictionary but  automatically creates a Pydantic model instance.
    #  The Pydantic model instance is NOT a dictionary (it’s an object).
    # Calling .model_dump() converts it back to a dictionary when needed.
     #  new_book=book_payload.model_dump()
     #  books.append(new_book)

      new_book=await book_service.create_book(book_payload,session)
      return new_book

@book_router.get('/book/{book_uid}',response_model=Book)
async def get_single_book(book_uid:str,session:AsyncSession=Depends(get_Session))->dict:
    book=await book_service.get_book(book_uid,session)
    if book:
      return book 
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Book not found")

@book_router.patch('/book/{book_uid}',response_model=Book)
async def update_single_book(book_uid:str,book_payload:UpdateBook,session:AsyncSession=Depends(get_Session))->dict:
   update_book=await book_service.update_book(book_uid,book_payload,session)
   if update_book is None:
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Book not found")
   else:
          return update_book
        
          

@book_router.delete('/book/{book_uid}')
async def delete_single_book(book_uid:str,session:AsyncSession=Depends(get_Session))->dict:
      delete_book=await book_service.delete_book(book_uid,session)
      print(f"{delete_book}-------------")
      if delete_book is None:
           raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Book not found")
      else:
          return {"message":"Book deleted successfully"}



# It modifies the behavior of a function without changing its code.
# In FastAPI, decorators like @app.get("/route") register the function as a route (API endpoint).

# @book_router.get('/get_headers',status_code=201)
# async def get_headers(
#     accept:str=Header(None),
#     content_type:str=Header(None)
#     # Header(None) means these headers are optional.

# ):
#     request_headers={
#         "Accept":accept,
#         "Content-Type":content_type
#     }
#     return request_headers


# @app.get('/greet/{name}')
# async def greetName(name:str)->dict:
#     return {'message':f"Hello {name}"}
# , /dinu chai api endpoint nai ho, tara query params ma chai dina pardaina 

# @book_router.get('/greet')
# async def greetName(name:Optional[str]="Ashesh",age:int=0)->dict:
#     return {'message':f"Hello {name}","age":age}

# class UserCreateModel(BaseModel):
#     name:str
#     job_title:str

# @book_router.post('/create_user')
# async def create_user(user_data:UserCreateModel):
#     return{
#         "name":user_data.name,
#         "job_title":user_data.job_title
#     }

