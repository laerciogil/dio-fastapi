from pydantic import BaseModel
from datetime import datetime, UTC

class PostRequest(BaseModel):
    title: str
    content: str
    published_at: datetime | None = None
    published: bool = False

class PostUpdateRequest(BaseModel):
    title: str | None = None
    content: str | None = None
    published_at: datetime | None = None
    published: bool | None = None