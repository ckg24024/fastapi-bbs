from pydantic import BaseModel

# ThreadBase：共通部分（title）
class ThreadBase(BaseModel):
    title: str

# ThreadCreate(ThreadBaseを継承)：新規作成時に使う（まだ id は無い）
class ThreadCreate(ThreadBase):
    pass
# ThreadResponse(ThreadBaseを継承)：一覧や詳細で返すデータ（id がある）
class ThreadResponse(ThreadBase):
    id: int