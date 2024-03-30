from fastapi import FastAPI
from contextlib import asynccontextmanager
from core.db import db
from api import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 서버 시작 전 초기화 단계 작성
    db.initialize()
    await db.create_database()
    yield
    # Clean up the ML models and release the resources


app = FastAPI(lifespan=lifespan)
app.include_router(api_router)


@app.get("/")
def hc():
    return "server is running"
