from pydantic import BaseModel
from datetime import datetime, UTC

class PostRequest(BaseModel):
    title: str
    date: datetime = datetime.now(UTC)
    published: bool = False