from fastapi import APIRouter
from app.schemas.thread import ThreadResponse, ThreadCreate

router = APIRouter(
    prefix="/threads",
    tags=["Threads"]
)


@router.get("/", response_model=list[ThreadResponse])
async def list_threads():
    """
    スレッド一覧（ダミー）
    将来はDBから取得するが、今は固定のJSONを返す。
    """
    return [
        {"id": 1, "title": "ダミースレッド1", "created_at": "2025-11-20T00:00:00"},
        {"id": 2, "title": "ダミースレッド2", "created_at": "2025-11-21T00:00:00"},
    ]


@router.get("/{thread_id}", response_model=ThreadResponse)
async def get_thread(thread_id: int):
    """
    スレッド詳細（ダミー）
    ThreadResponse で定義されたフィールドだけ返す。
    """
    return {
        "id": thread_id,
        "title": f"ダミースレッド{thread_id}",
        "created_at": "2025-11-21T00:00:00"
    }



@router.post("/", response_model=ThreadResponse)
async def create_thread(thread: ThreadCreate):
    """
    スレッド作成（ダミー）
    本当はタイトルや本文を受け取ってDBに保存する。
    今は '作成されたことにする' だけ。
    """
    return {
        "id": 999,
        "title": thread.title,
        "created_at": "2025-11-21T00:00:00",
    }
  