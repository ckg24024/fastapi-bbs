from app.database import engine, Base
from app.models.thread import Thread
from app.models.post import Post

def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()
    print("DB initialized.")