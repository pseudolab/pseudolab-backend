from fastapi import FastAPI
from fastapi.responses import JSONResponse
from app.api import routers

app = FastAPI()


@app.get("/")
def hc():
    return "server is running"


for router in routers:
    app.include_router(router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", env_file="config/.env")
