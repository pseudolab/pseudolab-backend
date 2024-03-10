from api import auth
from api.bingo.meta_word import bingo_router

routers = [auth.router, bingo_router]
