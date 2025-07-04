import os
from typing import List
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
from app.chroma_service import ChromaService

class DocumentIngestionService:
    def __init__(self, chroma_service: ChromaService):
        self.chroma_service = chroma_service
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')  # Replace with your preferred model

    def extract_text_from_pdf(self, file_path: str) -> str:
        """
        Extract text from a PDF file using PyPDF2.

        Args:
            file_path (str): Path to the PDF file.

        Returns:
            str: Extracted text from the PDF.
        """
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text

    def split_text(self, text: str, chunk_size: int = 500) -> List[str]:
        """
        Split text into smaller chunks for embedding.

        Args:
            text (str): The text to split.
            chunk_size (int): Maximum size of each chunk.

        Returns:
            List[str]: List of text chunks.
        """
        chunks = []
        current_chunk = []
        current_length = 0

        for sentence in text.split(". "):  # Split by sentences
            if not sentence.strip():  # Skip empty sentences
                continue
            if current_length + len(sentence) > chunk_size:
                chunks.append(" ".join(current_chunk))
                current_chunk = []
                current_length = 0
            current_chunk.append(sentence)
            current_length += len(sentence)

        if current_chunk:  # Add the last chunk
            chunks.append(" ".join(current_chunk))

        return chunks

    def generate_embeddings(self, text_chunks: List[str]) -> List[List[float]]:
        """
        Generate embeddings for a list of text chunks using Sentence Transformers.

        Args:
            text_chunks (List[str]): List of text chunks.

        Returns:
            List[List[float]]: List of embeddings.
        """
        return self.embedding_model.encode(text_chunks)

    def ingest_document(self, file_content: bytes, filename: str, username: str = None):
        """
        Process a document: extract text, split it, generate embeddings, and store in ChromaDB.

        Args:
            file_content (bytes): Content of the document file.
            filename (str): Name of the document file.
        """
        try:
            # Step 1: Extract text from the document
            print(f"Processing document '{filename}'...")
            text = self.extract_text_from_pdf(file_content)

            # Step 2: Split the text into chunks
            text_chunks = self.split_text(text)
            print(f"Extracted {len(text_chunks)} chunks from document '{filename}'.")

            # Step 3: Generate embeddings for the text chunks
            embeddings = self.generate_embeddings(text_chunks)

            # Step 4: Add text chunks and embeddings to ChromaDB
            self.chroma_service.add_document(content=text_chunks, filenames=[filename] * len(text_chunks), embedding=embeddings, username=username)


            print(f"Document '{filename}' ingested successfully!")
        except Exception as e:
            print(f"Error ingesting document '{filename}': {str(e)}")