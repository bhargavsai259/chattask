from fastapi import FastAPI

app = FastAPI(title="ChatTask Manager")

@app.get("/")
def health_check():
    return {"status": "ok"}
