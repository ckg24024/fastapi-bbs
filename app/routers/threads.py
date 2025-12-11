from fastapi import APIRouter,Depends
from app.models.thread import Thread
from app.schemas.thread import ThreadResponse, ThreadCreate
from app.database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import select, insert

router = APIRouter(
    prefix="/threads",
    tags=["Threads"]
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
    result = db.execute(stmt).scalar_one()
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