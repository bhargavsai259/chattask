from app.services.embeddings import EmbeddingService

embedding_service = EmbeddingService()

def build_task_text(title: str, description: str | None, time: str | None):
    parts = [title]
    if description:
        parts.append(description)
    if time:
        parts.append(time)
    return " ".join(parts)

def generate_task_embedding(title, description, time):
    text = build_task_text(title, description, time)
    return embedding_service.embed(text)
