import chromadb
import uuid

class ChromaService:
    def __init__(self, persist_directory="./chroma_storage"):
        self.client = chromadb.PersistentClient(
            path=persist_directory
        )
        self.collection = self.client.get_or_create_collection(name="docs")
        print(f"Collection created or retrieved: {self.collection.name}")

    def add_document(self, content: str, filename: str):
        # Generate a unique ID for the document
        unique_id = str(uuid.uuid4())

        """
        Add a document and its embedding to ChromaDB.
        """
        self.collection.add(
            documents=[content],
            metadatas=[{"filename": filename}],
            ids=[unique_id]
            # embeddings=[embedding]
        )
        print(f"Document added with ID: {unique_id}")

    def query_documents(self, query: str, n_results: int = 5):
        """
        Query ChromaDB for similar documents based on embeddings.
        """
        return self.collection.query(
            query_texts=[query],
            n_results=n_results
        )

    def query_documents_embeddings(self, query_embedding: list, n_results: int = 5):
        """
        Query ChromaDB for similar documents based on embeddings.
        """
        return self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )

    def get_collection(self):
        return self.collection.get()