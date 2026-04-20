from _typeshed import Incomplete
from contextlib import asynccontextmanager
from dio_blog.controller import auth as auth, post as post
from dio_blog.database import database as database, engine as engine, metadata as metadata
from fastapi import FastAPI

@asynccontextmanager
async def lifespan(app: FastAPI): ...

app: Incomplete

def run() -> None: ...
