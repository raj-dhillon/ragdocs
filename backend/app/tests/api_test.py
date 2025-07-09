import pytest
from fastapi.testclient import TestClient

from app.app import app  # Assuming your FastAPI app is defined in app/main.py

client = TestClient(app)

# Test case for the default route
def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to RAGDocs API!"}

# Currently writes to the database, which is not ideal for unit tests.
# To avoid this, we can mock the ingestion service or use a test database.
# For now, we will test the upload endpoint with a real file.
def test_upload_file():
    with open("app/tests/test_files/aws_cheatsheet.pdf", "rb") as f:
        response = client.post("/upload", params={"username": "test"}, files={"file": ("aws_cheatsheet.pdf", f, "application/pdf")})
    assert response.status_code == 201
    assert response.json() == {"message": "Document 'aws_cheatsheet.pdf' ingested successfully into `test` collection!"}

# Test case for uploading an invalid file type
def test_upload_invalid_file():
    response = client.post("/upload", files={"file": ("invalid.txt", "This is not a PDF file.", "text/plain")})
    assert response.status_code == 422
    assert response.json() == {"message": "Only PDF files are allowed."}

# Test case for querying documents
def test_query_docs():
    response = client.get("/querydocs", params={"query": "AWS"})
    assert response.status_code == 200
    assert "results" in response.json()

# Test case for querying documents with a llm response
def test_query():
    response = client.get("/query", params={"query": "What is AWS?"})
    assert response.status_code == 200
    assert "results" in response.json()