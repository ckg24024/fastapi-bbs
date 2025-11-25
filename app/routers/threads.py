from fastapi import APIRouter

router = APIRouter(
    prefix="/threads",
    tags=["Threads"]
)


@router.get("/")
async def list_threads():
    """
    スレッド一覧（ダミー）
    将来はDBから取得するが、今は固定のJSONを返す。
    """
    return [
        {"id": 1, "title": "ダミースレッド1"},
        {"id": 2, "title": "ダミースレッド2"},
    ]


@router.get("/{thread_id}")
async def get_thread(thread_id: int):
    """
    スレッド詳細（ダミー）
    """
    return {
        "id": thread_id,
        "title": f"ダミースレッド{thread_id}",
        "message": "ここに将来、投稿一覧などが入る予定です。",
    }


@router.post("/")
async def create_thread():
    """
    スレッド作成（ダミー）
    本当はタイトルや本文を受け取ってDBに保存する。
    今は '作成されたことにする' だけ。
    """
    return {"status": "ok", "message": "仮のスレッド作成APIです。"}
