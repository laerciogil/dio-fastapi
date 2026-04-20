from datetime import UTC as UTC, datetime
from pydantic import BaseModel

class PostRequest(BaseModel):
    title: str
    content: str
    published_at: datetime | None
    published: bool

class PostUpdateRequest(BaseModel):
    title: str | None
    content: str | None
    published_at: datetime | None
    published: bool | None
