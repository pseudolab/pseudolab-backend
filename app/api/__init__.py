from api import auth
from api.bingo.meta_word.routes import meta_word_router
from api.bingo.bingo_boards.routes import bingo_boards_router

routers = [auth.router, meta_word_router, bingo_boards_router]
