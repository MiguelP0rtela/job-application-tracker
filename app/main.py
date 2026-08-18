from fastapi import FastAPI
from app.routers import users
from sqlalchemy import text

from app.database.database import engine

app = FastAPI(
    title="Job Application Tracker API",
    version="1.0.0",
)

app.include_router(users.router)


@app.get("/health")
def health_check():
    return {"status": "ok"}
