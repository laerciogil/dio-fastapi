from typing import Annotated
from datetime import datetime, UTC

from fastapi import Response, status, Cookie, Header, APIRouter

from view.post import PostResponse
from schemas.post import PostRequest

router = APIRouter(prefix="/posts", tags=["Posts"])

fake_db = [
    {"title": "Criando uma aplicação com Django",
     "date": datetime.now(UTC),
     "published": True},
    {"title": "Internacionalizando apps com FastAPI",
     "date": datetime.now(UTC),
     "published": True},
    {"title": "Criando uma aplicação com Flask",
     "date": datetime.now(UTC),
     "published": True},
    {"title": "Internacionalizando apps com Starlette",
     "date": datetime.now(UTC),
     "published": False}
]

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
def create_post(post: PostRequest):
    fake_db.append(post.model_dump())
    return post

@router.get("/", response_model=list[PostResponse])
def read_posts(response: Response, 
               published: bool, 
               limit: int, 
               skip: int = 0,
               ads_id: Annotated[str | None, Cookie()] = None,
               user_agent: Annotated[str | None, Header()] = None
               ):
    response.set_cookie(key="user", value="user@gmail.com")
    print(f"Cookie: {ads_id}")
    print(f"User-Agent: {user_agent}")
    return [post for post in fake_db[skip:skip + limit] if post["published"] is published]

@router.get("/{framework}", response_model=PostResponse)
def read_framework_posts(framework: int):
    return {"posts": [{"title": f"Criando uma aplicação com {framework}",
                       "date": datetime.now(UTC)},
                       {"title": f"Internacionalizando apps com {framework}",
                       "date": datetime.now(UTC)}]}