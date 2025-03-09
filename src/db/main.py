# This code is setting up an asynchronous database connection using SQLModel and SQLAlchemy.
# SQLAlchemy is a Python library for working with databases.lie typeorm,Interacts with tables using Python classes.
#  An engine in SQLAlchemy is the core database connection that allows your application to interact with the database.

from sqlmodel import create_engine,text,SQLModel
from sqlalchemy.ext.asyncio import AsyncEngine
from src.config import Config

engine =AsyncEngine(
    create_engine(
    url=Config.DATABASE_URL,
    echo=True 
    # echo true means like console.log in server
))

async def init_db():
    async with engine.begin() as conn:
        from src.books.models import Book
      
        await conn.run_sync(SQLModel.metadata.create_all)