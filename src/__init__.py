from fastapi import FastAPI
from src.books.routes import book_router
from src.db.main import init_db
from contextlib import asynccontextmanager
# In FastAPI, asynccontextmanager is commonly used for startup and shutdown events in the application.

@asynccontextmanager
async def life_span(app:FastAPI):
    print(f"server is starting...")
    await init_db()
    yield
    print(f"server has been stopped ..")

version ="v1"

app=FastAPI(
    title="Asheshdon",
    description ="rest api for fast api",    
    version=version,
    lifespan=life_span
)

app.include_router(book_router,prefix=f"/api/{version}",tags=["books"])