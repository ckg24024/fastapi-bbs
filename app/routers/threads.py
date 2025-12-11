from fastapi import APIRouter, Depends, HTTPException, Request
from app.models.thread import Thread
from app.models.post import Post
from app.schemas.thread import ThreadResponse, ThreadCreate
from app.database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import select, insert

router = APIRouter(
    prefix="/threads",
    tags=["Threads"]
)

from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
# -----------------------------------
# フロント側処理 一覧
# -----------------------------------
templates = Jinja2Templates(directory="app/templates")
@router.get("/list", response_class=HTMLResponse)
async def list_threads_page(request: Request, db: Session = Depends(get_db)):

    # スレッドの一覧を新しい順に取得
    stmt = select(Thread).order_by(Thread.created_at.desc())
    threads = db.execute(stmt).scalars().all()

    # --- 最新投稿10件を取得（ThreadとJOIN） ---
    stmt_posts = (
        select(
            Post.id,
            Post.content,
            Post.author,
            Post.created_at,
            Thread.title.label("thread_title"),
            Thread.id.label("thread_id")
        )
        .join(Thread, Thread.id == Post.thread_id)
        .order_by(Post.created_at.desc())
        .limit(10)
    )

    latest_posts = db.execute(stmt_posts).all()

    return templates.TemplateResponse(
        "index.html",
        {"request": request,
        "threads": threads,
        "latest_posts": latest_posts}
    )


# -----------------------------------
# スレッド一覧 GET /threads
# -----------------------------------
@router.get("/", response_model=list[ThreadResponse])
async def list_threads(db: Session = Depends(get_db)):
    stmt = select(Thread)
    result = db.execute(stmt).scalars().all()
    return result

# -----------------------------------
# スレッド詳細 GET /threads/{thread_id}
# -----------------------------------
@router.get("/{thread_id}", response_model=ThreadResponse)
async def get_thread(thread_id: int, db: Session = Depends(get_db)):
    stmt = select(Thread).where(Thread.id == thread_id)
    result = db.execute(stmt).scalar_one_or_none()

    if result is None:
        # 見つからないので例外を raise 404 Not found
        raise HTTPException(status_code=404, detail="Thread not found")

    return result

# -----------------------------------
# スレッド作成 POST /threads
# -----------------------------------
@router.post("/", response_model=ThreadResponse)
async def create_thread(thread: ThreadCreate,db: Session = Depends(get_db)):
    # INSERT
    stmt = insert(Thread).values(title=thread.title)
    result = db.execute(stmt)
    db.commit()

    # 実行結果からidを取得(AUTOINCREMENT で生成された id を取得)
    new_id = result.lastrowid

    # 今作ったレコードを読み直し
    stmt2 = select(Thread).where(Thread.id == new_id)
    new_thread = db.execute(stmt2).scalar_one()
    return new_thread
