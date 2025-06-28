from fastapi import FastAPI, UploadFile

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to my FastAPI application!"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "query": q}

@app.post("/upload")
async def upload_file(file: UploadFile):
        return {"filename": file.filename, "content_type": file.content_type}

@app.get("/query")
def get_query(query: str):
    return {"query": query}