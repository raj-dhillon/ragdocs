from fastapi import FastAPI, UploadFile
from app.chroma_service import ChromaService
from app.doc_ingestion import DocumentIngestionService
from io import BytesIO
from app.llm_service import OllamaService

app = FastAPI()

# Initialize ChromaDB service
chroma_service = ChromaService()
# Initialize Document Ingestion Service
doc_ingestion_service = DocumentIngestionService(chroma_service=chroma_service)
# Initialize LLM Service
llm_service = OllamaService(model="llama3.2")

@app.get("/")
def read_root():
    return {"message": "Welcome to my FastAPI application!"}

@app.post("/upload")
async def upload_file(file: UploadFile):
        """
        Upload a file, generate embeddings, and store it in ChromaDB.
        """

        if not file.filename.endswith(".pdf"):
            return {"message": "Only PDF files are allowed."}
        
        try:
            # Read file content
            content = await file.read()
            pdf_file = BytesIO(content)

            # Ingest the document
            doc_ingestion_service.ingest_document(file_content=pdf_file, filename=file.filename)

            return {"message": f"Document '{file.filename}' ingested successfully!"}
        except Exception as e:
            return {"error": str(e)}


@app.get("/querydocs")
def get_query_docs(query: str):
    """
    Query ChromaDB for similar documents based on embeddings.
    """
    try:
        # Search for similar documents in ChromaDB
        results = chroma_service.query_documents(query=query, n_results=5)

        return {"results": results}
    except Exception as e:
        return {"error": str(e)}
    
@app.get("/query")
def get_query(query: str):
    """
    Query ChromaDB for similar documents based on embeddings, and return LLM answer.
    """
    try:
        # Search for similar documents in ChromaDB
        context = chroma_service.query_documents(query=query, n_results=5)
        if not context:
            return {"message": "No relevant documents found."}
        # Generate response using LLM
        response = llm_service.generate_response(query=query, context=context["documents"][0])
        

        return {"results": response}
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
    