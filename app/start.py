import dotenv

dotenv.load_dotenv("config/.env")

from main import app


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", reload=True, workers=4)
