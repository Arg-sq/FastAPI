# This code is setting up an asynchronous database connection using SQLModel and SQLAlchemy.
# SQLAlchemy is a Python library for working with databases.like typeorm,Interacts with tables using Python classes.
#  An engine in SQLAlchemy is the core database connection that allows your application to interact with the database.

from sqlmodel import create_engine,SQLModel
from sqlalchemy.ext.asyncio import AsyncEngine
from src.config import Config
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker

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

async def get_Session()->AsyncSession:
    Session=sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False
    )
    async with Session() as session:
        yield session
        # If we used return session, the session wouldn’t be properly closed after use.
        # yield allows FastAPI to manage session cleanup automatically.
        # FastAPI automatically calls get_Session()