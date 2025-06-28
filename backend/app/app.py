from fastapi import FastAPI, UploadFile
from app.chroma_service import ChromaService

app = FastAPI()

# Initialize ChromaDB service
chroma_service = ChromaService()

@app.get("/")
def read_root():
    return {"message": "Welcome to my FastAPI application!"}

@app.post("/upload")
async def upload_file(file: UploadFile):
        # return {"filename": file.filename, "content_type": file.content_type}
        """
        Upload a file, generate embeddings, and store it in ChromaDB.
        """
        try:
            # Read file content
            content = await file.read()
            content_str = content.decode("utf-8")  # Assuming text files

            # # Generate embeddings (replace with your embedding function)
            # embedding = [0.1, 0.2, 0.3]  # Example embedding, replace with actual function

            # Store document and embeddings in ChromaDB
            chroma_service.add_document(content=content_str, filename=file.filename)

            return {"message": f"File '{file.filename}' uploaded and stored successfully!"}
        except Exception as e:
            return {"error": str(e)}


@app.get("/query")
def get_query(query: str):
    # return {"query": query}
    """
    Query ChromaDB for similar documents based on embeddings.
    """
    try:
        # # Generate embeddings for the query
        # query_embedding = [0.1, 0.2, 0.3]  # Example embedding, replace with actual function

        # Search for similar documents in ChromaDB
        results = chroma_service.query_documents(query=query, n_results=5)

        return {"results": results}
    except Exception as e:
        return {"error": str(e)}

@app.get("/collection")
def get_collection():
    """
    Get the collection from ChromaDB.
    """
    try:
        collection = chroma_service.get_collection()
        return {"collection": collection}
    except Exception as e:
        return {"error": str(e)}