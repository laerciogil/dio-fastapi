from pydantic import BaseModel
from datetime import datetime, UTC

class PostResponse(BaseModel):
    title: str
    date: datetime