from sqlmodel.ext.asyncio.session import AsyncSession
from .book_schema import BookCreateModel,UpdateBook
from .models import Book
from sqlmodel import select,desc
from datetime import datetime
# A session in SQLAlchemy (and SQLModel) is like a database transaction manager. It:
# 
# Manages database connections.
# Allows us to query and modify data.
# Keeps track of pending changes before committing to the database.
class BookService:
    # class bhitra ko func are methods
    async def get_all_books(self,session:AsyncSession):
        statement=select(Book).order_by(desc(Book.created_at))

        result= await session.exec(statement)
        return result.all()

    async def get_book(self,book_uid:str,session:AsyncSession):
       
        statement=select(Book).where(Book.uid == book_uid)
       
        result =await session.exec(statement)
        book=result.first()

        return book if book is not None else {}
    
    async def create_book(self,book_payload:BookCreateModel,session:AsyncSession):
        book_payload_dict=book_payload.model_dump()

        new_book=Book(**book_payload_dict)

        new_book.published_date=datetime.strptime(book_payload_dict['published_date'],"%Y-%m-%d")
        session.add(new_book)
        await session.commit()

        return new_book
    
    async def update_book(self,book_uid:str,book_payload:UpdateBook,session:AsyncSession):
        # accessing methods of class
        book_to_update=await self.get_book(book_uid,session)
        if book_to_update is not None:
            update_data_dict=book_payload.model_dump()
            for key,value in update_data_dict.items():
                    setattr(book_to_update,key,value)
                
            await session.commit()
            return book_to_update
        else:
             return None
    
    async def delete_book(self,book_uid:str,session:AsyncSession):
        book_to_delete=await self.get_book(book_uid,session)
        if book_to_delete is not None:
             await session.delete(book_to_delete)
             await session.commit()
             return {} 
        else:
             return None
    