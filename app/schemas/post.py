from pydantic import BaseModel
from datetime import datetime

# 共通部分
class PostBase(BaseModel):
    author: str | None = None
    content: str
    parent_post_id: int | None = None

# 新規作成用
class PostCreate(PostBase):
    post_number:int


# レスポンス用
class PostResponse(PostBase):
    id: int
    thread_id: int
    post_number: int
    created_at: datetime
    attachment: str | None = None