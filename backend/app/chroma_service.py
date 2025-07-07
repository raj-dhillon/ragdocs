import chromadb
import uuid
import os
from dotenv import load_dotenv

class ChromaService:
    def __init__(self):
        load_dotenv()  # Load environment variables from .env file
        persist_directory = os.getenv("CHROMA_STORAGE_PATH", "./chroma_storage")
        self.client = chromadb.PersistentClient(path=persist_directory)
        self.default_collection = self.client.get_or_create_collection(name="docs")
        print(f"Default collection created or retrieved: {self.default_collection.name}")
    
    def get_or_create_collection(self, username: str):
        """
        Get or create a collection in ChromaDB using the provided username as the collection name.
        """
        if username:
            return self.client.get_or_create_collection(name=username)
        return self.default_collection
        
    def add_document(self, content: str, filenames: str, embedding: list = None, username: str = None):
        """
        Add a document and its embedding to ChromaDB.
        """

        # Get the correct collection based on the username
        collection = self.get_or_create_collection(username)
        
        # Generate a unique ID for the document
        ids = [str(uuid.uuid4()) for _ in filenames]

        add_args = {
            "documents": content,
            "metadatas": [{"filename": filename} for filename in filenames],
            "ids": ids,
        }
        if embedding is not None:
            add_args["embeddings"] = embedding

        collection.add(**add_args)
        print(f"Added {len(content)} chunks to collection `{collection}`.")

    def query_documents(self, query: str, n_results: int = 5, username: str = None):
        """
        Query ChromaDB for similar documents based on embeddings.
        """

        # Get the correct collection based on the username
        collection = self.get_or_create_collection(username)

        return collection.query(
            query_texts=[query],
            n_results=n_results,
            include=["documents", "metadatas"]
        )

    def query_documents_embeddings(self, query_embedding: list, n_results: int = 5, username: str = None):
        """
        Query ChromaDB for similar documents based on embeddings.
        """

        # Get the correct collection based on the username
        collection = self.get_or_create_collection(username)

        return collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )

    def get_collection(self, username: str = None):
        collection = self.get_or_create_collection(username)
        return collection.get()
