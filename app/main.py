from fastapi import FastAPI
from app.db.base import engine
from app.db import model
from app.api.tasks import router as task_router
from app.services.embeddings import EmbeddingService


model.Base.metadata.create_all(bind=engine)

app = FastAPI(title="ChatTask Manager")
embedding_service = EmbeddingService()


app.include_router(task_router)

@app.get("/")
def health_check():
    return {"status": "ok"}

@app.get("/test-embed")
def test_embed():
    vec = embedding_service.embed("Christmas morning gift distribution")
    return {"length": len(vec)}
