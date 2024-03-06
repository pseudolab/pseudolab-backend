from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.core.db import db
from app.api import routers


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 서버 시작 전 초기화 단계 작성
    db.initialize()
    yield
    # Clean up the ML models and release the resources


app = FastAPI(lifespan=lifespan)


@app.get("/")
def hc():
    return "server is running"


for router in routers:
    app.include_router(router)
