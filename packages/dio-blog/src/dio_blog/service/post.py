from databases.interfaces import Record
from fastapi import HTTPException, status

from dio_blog.database import database
from dio_blog.model.post import posts
from dio_blog.schemas.post import PostRequest, PostUpdateRequest

class PostService:

    async def read_all(self, published: bool, limit: int, skip: int) -> list[Record]:
        query = posts.select().limit(limit).offset(skip).where(posts.c.published == published)
        return await database.fetch_all(query)
    
    async def read(self, id: int) -> Record:
        return await self.__get_by_id(id)
    
    async def create(self, post: PostRequest) -> int:
        command = posts.insert().values(**post.model_dump())
        return await database.execute(command)
    
    async def update(self, id: int, post: PostUpdateRequest) -> Record:
        command = posts.update().where(posts.c.id == id).values(**post.model_dump(exclude_unset=True))
        await database.execute(command)
        return await self.__get_by_id(id)

    async def delete(self, id: int) -> None:
        command = posts.delete().where(posts.c.id == id)
        await database.execute(command)

    async def __count(self, id: int) -> int:
        query = "SELECT COUNT(*) total FROM posts WHERE id = :id"
        result = await database.fetch_one(query, values={"id": id})
        return result["total"] if result else 0

    async def __get_by_id(self, id: int) -> Record:
        query = posts.select().where(posts.c.id == id)
        post = await database.fetch_one(query)
        if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
        return post