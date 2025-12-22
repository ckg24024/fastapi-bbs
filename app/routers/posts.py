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


from fastapi import Form, File, UploadFile, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
import os

UPLOAD_DIR = "app/static/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

templates = Jinja2Templates(directory="app/templates")
# -----------------------
# 投稿作成（通常 or 返信）
# POST /threads/{thread_id}/posts
# -----------------------
@threads_router.post("/{thread_id}/post", response_class=HTMLResponse)
async def create_new_post(
    request: Request,
    thread_id: int,
    author: str = Form(""),
    content: str = Form(...),
    parent_post_id: int | None = Form(None),
    image: UploadFile | None = File(None),
    parent_post_id_hidden: int | None = Form(None),
    db: Session = Depends(get_db)):
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

    # (1.5)添付ファイル処理
    attachment_filename = None
    if image and image.filename:
        # ファイル名の決定
        _,ext = os.path.splitext(image.filename)
        filename = f"thread{thread_id}_post{next_number}{ext}"
        save_path = os.path.join(UPLOAD_DIR,filename)

        # 保存
        with open(save_path,"wb") as f:
            f.write(await image.read())
        attachment_filename = filename


    # 追加 INSERT
    # (2) Post（本文）作成
    values = {
        "thread_id": thread_id,
        "content": content,
        "post_number":next_number,
    }

    # author 空欄なら DEFAULT '名無しさん' を使う
    if author.strip():
        values["author"] = author

    # 返信番号があれば返信
    if parent_post_id_hidden:
        values["parent_post_id"] = parent_post_id_hidden

    # 添付ファイルがあれば追加
    if attachment_filename:
        values["attachment"] = attachment_filename

    result = db.execute(insert(Post).values(values))

    db.commit()

    new_id = result.lastrowid

    # 登録した投稿を取得して返す
    stmt_new = select(Post).where(Post.id == new_id)
    new_post = db.execute(stmt_new).scalar_one()

    # (3) スレッド詳細へリダイレクト
    return RedirectResponse(
        url=f"/threads/{thread_id}/view",
        status_code=303
    )