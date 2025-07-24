from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/query")
def query(text: str):
    # placeholder for RAG query logic
    return {"answer": "This is a stub."}
