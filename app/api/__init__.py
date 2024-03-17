from api import auth
from api.bingo.meta_word import bingo_router
from api.bingo.bingo_boards import bingo_board_router

routers = [auth.router, bingo_router, bingo_board_router]
