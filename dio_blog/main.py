import sqlalchemy as sa
import databases

from fastapi import FastAPI
from contextlib import asynccontextmanager

from dio_blog.controller.post import router as post_router

DATABASE_URL = "sqlite:///./blog.db"

database = databases.Database(DATABASE_URL)
metadata = sa.MetaData()
engine = sa.create_engine(DATABASE_URL, echo=True, connect_args={"check_same_thread": False})
metadata.create_all(engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    yield
    await database.disconnect()

app = FastAPI(title="DIO Blog API", 
              version="0.1.0", 
              description="API para gerenciamento de posts do blog da DIO",
              lifespan=lifespan)

app.include_router(post_router)