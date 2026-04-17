from fastapi import FastAPI
from contextlib import asynccontextmanager

from dio_blog.database import database, metadata, engine
from dio_blog.controller import auth, post

@asynccontextmanager
async def lifespan(app: FastAPI):
    from dio_blog.model.post import posts #noqa
    await database.connect()
    metadata.create_all(engine)
    yield
    await database.disconnect()

app = FastAPI(title="DIO Blog API", 
              version="0.1.0", 
              description="API para gerenciamento de posts do blog da DIO",
              lifespan=lifespan)

app.include_router(auth.router)
app.include_router(post.router)