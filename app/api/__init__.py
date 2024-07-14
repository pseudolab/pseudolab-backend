from fastapi import APIRouter

from api.auth import auth_router
from api.bingo.meta_word.routes import meta_word_router
from api.bingo.bingo_boards.routes import bingo_boards_router
from api.bingo.bingo_interaction.routes import bingo_interaction_router
from api.board.crud.routes import boards_router
from api.board.comment.routes import comments_router

api_router = APIRouter(prefix="/api")

routers = [auth_router, meta_word_router, bingo_boards_router, bingo_interaction_router, boards_router, comments_router]

for router in routers:
    api_router.include_router(router)
