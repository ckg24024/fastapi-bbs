from fastapi import APIRouter

from app.schemas.post import PostCreate, PostResponse

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


# -----------------------
# 投稿詳細（ダミー）
# -----------------------
@router.get("/{post_id}", response_model=PostResponse)
async def get_post(post_id: int):
    """
    投稿詳細（ダミー）
    """
    return {
        "id": post_id,
        "thread_id": 1,
        "post_number": 1,
        "content": f"ダミー投稿 {post_id} の内容です。",
        "parent_post_id": None,
        "created_at": "2025-11-21T00:00:00"
    }


# =======================
# Threads に紐づくルート
# =======================

threads_router = APIRouter(
    prefix="/threads",
    tags=["Posts"]
)


# -----------------------
# スレッドの投稿一覧
# -----------------------
@threads_router.get("/{thread_id}/posts", response_model=list[PostResponse])
async def list_posts(thread_id: int):
    """
    指定スレッドの投稿一覧（ダミー）
    """
    return [
        {
            "id": 1,
            "thread_id": thread_id,
            "post_number": 1,
            "content": "ダミー投稿1",
            "parent_post_id": None,
            "created_at": "2025-11-21T00:00:00",
        },
        {
            "id": 2,
            "thread_id": thread_id,
            "post_number": 2,
            "content": "ダミー投稿2（返信）",
            "parent_post_id": 1,
            "created_at": "2025-11-21T00:00:00",
        },
    ]


# -----------------------
# 投稿作成（通常 or 返信）
# -----------------------
@threads_router.post("/{thread_id}/posts", response_model=PostResponse)
async def create_post(thread_id: int, post: PostCreate):
    """
    投稿作成（ダミー）
    parent_post_id が None → 通常投稿
    parent_post_id が番号 → 返信
    """
    return {
        "id": 999,
        "thread_id": thread_id,
        "post_number": 999,  # 本当はDBで決まる
        "content": post.content,
        "parent_post_id": post.parent_post_id,
        "created_at": "2025-11-21T00:00:00",
    }