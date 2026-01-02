import faiss
import numpy as np
from app.db.model import Task
from app.db.base import SessionLocal
from app.services.task_embedding import embedding_service

class SimilaritySearch:
    def __init__(self):
        self.dimension = 384  # embedding size of all-MiniLM-L6-v2
        self.index = faiss.IndexFlatL2(self.dimension)
        self.task_ids = []
        self.load_index()

    def load_index(self):
        """Load all task embeddings from DB into FAISS"""
        db = SessionLocal()
        tasks = db.query(Task).all()
        embeddings = []
        
        # Reset the index and task_ids for fresh load
        self.index = faiss.IndexFlatL2(self.dimension)
        self.task_ids = []

        for task in tasks:
            if task.embedding:
                vec = np.array(eval(task.embedding), dtype="float32")
                embeddings.append(vec)
                self.task_ids.append(task.id)

        if embeddings:
            self.index.add(np.vstack(embeddings))
        db.close()

    def search(self, query_text, top_k=1):
        # Reload index before searching to get latest tasks
        self.load_index()
        
        query_vec = np.array([embedding_service.embed(query_text)], dtype="float32")
        D, I = self.index.search(query_vec, top_k)
        results = []
        for idx in I[0]:
            if idx < len(self.task_ids):
                results.append(self.task_ids[idx])
        return results
