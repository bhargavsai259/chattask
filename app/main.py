from fastapi import FastAPI
from app.db.base import engine
from app.db import model
from app.api.tasks import router as task_router

model.Base.metadata.create_all(bind=engine)

app = FastAPI(title="ChatTask Manager")

app.include_router(task_router)

@app.get("/")
def health_check():
    return {"status": "ok"}
