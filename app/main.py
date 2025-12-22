from fastapi import FastAPI
from app.routers import threads
from app.routers import posts
from fastapi.staticfiles import StaticFiles

app = FastAPI(
    title="BBS API",
    description="Simple Bulletin Board System API",
    version="0.1"
)


app.include_router(threads.router)
app.include_router(posts.router)
app.include_router(posts.threads_router)
app.mount("/static", StaticFiles(directory="app/static"), name="static")