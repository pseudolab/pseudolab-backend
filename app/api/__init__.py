from api import auth
from api.bingo import bingo_router

routers = [auth.router, bingo_router]
