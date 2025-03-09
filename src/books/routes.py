from fastapi import APIRouter,status
from fastapi.exceptions import HTTPException
from src.books.book_data import books
from src.books.book_schema import Book,UpdateBook
from typing import List

book_router=APIRouter()

@book_router.get('/books',response_model=List[Book])
async def get_all_books()->list:
    return books

@book_router.post('/add_books',status_code=status.HTTP_201_CREATED)
async def create_a_book(book_payload:Book)->dict:
    #   FastAPI does NOT pass payload directly as a dictionary but  automatically creates a Pydantic model instance.
    #  The Pydantic model instance is NOT a dictionary (it’s an object).
    # Calling .model_dump() converts it back to a dictionary when needed.
      new_book=book_payload.model_dump()
      books.append(new_book)
      return new_book

@book_router.get('/book/{book_id}')
async def get_single_book(book_id:int)->dict:
    for book in books:
         if book['id'] == book_id:
              return book
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Book not found")

@book_router.patch('/book/{book_id}')
async def update_single_book(book_id:int,book_payload:UpdateBook)->dict:
     for book in books:
          if book['id']==book_id:
               book['title']=book_payload.title
               book['author']=book_payload.author
               book['year']=book_payload.year
               book['genre']=book_payload.genre
               book['pages']=book_payload.pages
               
               return book
          
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Book not found")

@book_router.delete('/book/{book_id}')
async def delete_single_book(book_id:int)->dict:
      for book in books:
          if book['id']==book_id:
               books.remove(book)
               return {'message':'Book deleted successfully'}
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Book not found")
      



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

