from api.auth import auth_router
from fastapi import APIRouter

api_router = APIRouter(prefix="/api")


routers = [auth_router]

for router in routers:
    api_router.include_router(router)
