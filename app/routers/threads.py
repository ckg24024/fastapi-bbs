from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select, insert

from app.schemas.post import PostCreate, PostResponse
from app.database import get_db
from app.models.post import Post
from app.models.thread import Thread


router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


# -----------------------
# 投稿詳細 GET /posts/{post_id}
# -----------------------
@router.get("/{post_id}", response_model=PostResponse)
async def get_post(post_id: int, db: Session = Depends(get_db)):
    # SQLの組立
    stmt = select(Post).where(Post.id == post_id)
    # 存在しない場合があるのでscalar_one_or_none()
    post = db.execute(stmt).scalar_one_or_none()

    if post is None:
        # 見つからないので例外を raise 404 Not found
        raise HTTPException(status_code=404, detail="Post not found")

    return post

# =======================
# Threads に紐づくルート
# =======================

threads_router = APIRouter(
    prefix="/threads",
    tags=["Posts"]
)


# -----------------------
# スレッドの投稿一覧
# GET /threads/{thread_id}/posts
# -----------------------
@threads_router.get("/{thread_id}/posts", response_model=list[PostResponse])
async def list_posts(thread_id: int, db: Session = Depends(get_db)):
    # threadの存在チェック
    stmt_thread = select(Thread).where(Thread.id == thread_id)
    exists = db.execute(stmt_thread).scalar_one_or_none()

    if exists is None:
        # 見つからないので例外を raise 404 Not found
        raise HTTPException(status_code=404, detail="Thread not found")

    # Threadは確実にあるため、Threadに投稿されている投稿データをpost_numberの昇順に取得
    stmt = select(Post).where(Post.thread_id == thread_id).order_by(Post.post_number)
    posts = db.execute(stmt).scalars().all()

    return posts

# -----------------------
# 投稿作成（通常 or 返信）
# POST /threads/{thread_id}/posts
# -----------------------
@threads_router.post("/{thread_id}/posts", response_model=PostResponse)
async def create_post(thread_id: int, post: PostCreate, db: Session = Depends(get_db)):
    # threadの存在チェック
    stmt_thread = select(Thread).where(Thread.id == thread_id)
    exists = db.execute(stmt_thread).scalar_one_or_none()

    if exists is None:
        # 見つからないので例外を raise 404 Not found
        raise HTTPException(status_code=404, detail="Thread not found")

    # 次のpost_numberを取得
    stmt_last = (select(Post.post_number)
                .where(Post.thread_id == thread_id)
                .order_by(Post.post_number.desc())
                .limit(1)
    )

    last_number = db.execute(stmt_last).scalar_one_or_none()
    # 初回の投稿ならば1をそうでなければ、最後の投稿番号+1
    next_number = 1 if last_number is None else last_number + 1

    # 追加 INSERT
    stmt_insert = insert(Post).values(
        thread_id = thread_id,
        post_number = next_number,
        content = post.content,
        parent_post_id = post.parent_post_id
    )

    result = db.execute(stmt_insert)

    db.commit()

    new_id = result.lastrowid

    # 登録した投稿を取得して返す
    stmt_new = select(Post).where(Post.id == new_id)
    new_post = db.execute(stmt_new).scalar_one()

    return new_post