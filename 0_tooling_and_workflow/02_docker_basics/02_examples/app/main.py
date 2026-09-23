from fastapi import FastAPI

app = FastAPI(title="docker-basics-demo")


@app.get("/")
def read_root() -> dict:
    return {"status": "ok", "message": "Hello from Docker!"}


@app.get("/health")
def health() -> dict:
    return {"status": "healthy"}
