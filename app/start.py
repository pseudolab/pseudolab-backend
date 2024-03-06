from main import app

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", env_file="config/.env", reload=True, workers=1)
