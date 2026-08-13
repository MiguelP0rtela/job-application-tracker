from fastapi import FastAPI
from sqlalchemy import text

from app.database.database import engine

app = FastAPI(
    title="Job Application Tracker API",
    version="1.0.0",
)


@app.get("/health")
def health_check():
    return {"status": "ok"}
