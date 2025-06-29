import chromadb
import uuid

class ChromaService:
    def __init__(self, persist_directory="./chroma_storage"):
        self.client = chromadb.PersistentClient(
            path=persist_directory
        )
        self.collection = self.client.get_or_create_collection(name="docs")
        print(f"Collection created or retrieved: {self.collection.name}")

    def add_document(self, content: str, filenames: str, embedding: list = None):
        # Generate a unique ID for the document
        ids = [str(uuid.uuid4()) for _ in filenames]

        add_args = {
            "documents": content,
            "metadatas": [{"filename": filename} for filename in filenames],
            "ids": ids,
        }
        if embedding is not None:
            add_args["embeddings"] = embedding

        """
        Add a document and its embedding to ChromaDB.
        """
        self.collection.add(**add_args)
        print(f"Added {len(content)} chunks to ChromaDB.")

    def query_documents(self, query: str, n_results: int = 5):
        """
        Query ChromaDB for similar documents based on embeddings.
        """
        return self.collection.query(
            query_texts=[query],
            n_results=n_results,
            include=["documents", "metadatas"]
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
