from datetime import UTC as UTC, datetime
from pydantic import BaseModel

class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    published_at: datetime | None
