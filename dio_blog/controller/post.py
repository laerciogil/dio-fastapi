from fastapi import Response, status, APIRouter

from dio_blog.database import database
from dio_blog.view.post import PostResponse
from dio_blog.schemas.post import PostRequest, PostUpdateRequest
from dio_blog.model.post import posts
from dio_blog.service.post import PostService

service = PostService()
router = APIRouter(prefix="/posts", tags=["Posts"])

@router.get("/", response_model=list[PostResponse])
async def read_posts(published: bool = False, limit: int = 10, skip: int = 0):
    return await service.read_all(published, limit, skip)

@router.get("/{id}", response_model=PostResponse)
async def read_post(id: int):
    return await service.read(id)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
async def create_post(post: PostRequest):
    id = await service.create(post)
    return await service.read(id)

@router.put("/{id}", response_model=PostResponse)
async def update_post(id: int, post: PostUpdateRequest):
    return await service.update(id, post)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, response_model=None)
async def delete_post(id: int):
    await service.delete(id)