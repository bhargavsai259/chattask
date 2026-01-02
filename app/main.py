from fastapi import FastAPI
from app.db.base import engine
from app.db import model
from app.api.tasks import router as task_router
from app.services.embeddings import EmbeddingService
from app.services.similarity import SimilaritySearch



model.Base.metadata.create_all(bind=engine)

app = FastAPI(title="ChatTask Manager")
embedding_service = EmbeddingService()
similarity_service = SimilaritySearch()



app.include_router(task_router)

@app.get("/")
def health_check():
    return {"status": "ok"}

@app.get("/test-embed")
def test_embed():
    vec = embedding_service.embed("Christmas morning gift distribution")
    return {"length": len(vec)}


@app.get("/test-similarity")
def test_similarity(q: str):
    matched_task_ids = similarity_service.search(q)
    return {"matched_task_ids": matched_task_ids}