from fastapi import FastAPI
from fastapi.responses import JSONResponse


app = FastAPI()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", env_file="config/.env")
