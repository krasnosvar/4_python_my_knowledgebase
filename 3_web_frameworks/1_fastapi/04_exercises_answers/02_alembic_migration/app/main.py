from fastapi import FastAPI

from .routers import items

app = FastAPI(title="FastAPI example — items service")

app.include_router(items.router)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}
