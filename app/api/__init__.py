from app.api.auth import *
import app.api.auth.discord_login  # noqa

routers = [
    auth.router
]
