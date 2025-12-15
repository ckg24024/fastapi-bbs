from pydantic import BaseModel
from datetime import datetime
from app.schemas.post import PostCreate

# ThreadBase：共通部分（title）、投稿データ（post:PostCreate）
class ThreadBase(BaseModel):
    title: str
    post: PostCreate

# ThreadCreate(ThreadBaseを継承)：新規作成時に使う（まだ id は無い）
class ThreadCreate(ThreadBase):
    pass

# ThreadResponse(ThreadBaseを継承)：一覧や詳細で返すデータ（id がある）
class ThreadResponse(ThreadBase):
    id: int
    created_at:datetime