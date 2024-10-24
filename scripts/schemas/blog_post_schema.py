from typing import Optional

from pydantic import BaseModel


class BlogPost(BaseModel):
    post_id: Optional[int] = None  # ID will be assigned automatically
    title: str
    meta: Optional[dict] = {}
    content: Optional[str] = ""
    is_delete: Optional[bool] = False
