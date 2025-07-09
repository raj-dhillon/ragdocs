# import pytest
# from unittest.mock import MagicMock
# from app.doc_ingestion import DocumentIngestionService
# from app.chroma_service import ChromaService
# from io import BytesIO
# from fpdf import FPDF

# @pytest.fixture
# def mock_chroma_service():
#     """
#     Create a mock ChromaService for testing.
#     """
#     return MagicMock(spec=ChromaService)

# @pytest.fixture
# def doc_ingestion_service(mock_chroma_service):
#     """
#     Create a DocumentIngestionService instance with a mocked ChromaService.
#     """
#     return DocumentIngestionService(chroma_service=mock_chroma_service)

# def test_extract_text_from_pdf(doc_ingestion_service):
#     """
#     Test text extraction from a PDF file.
#     """
#     # Mock PDF content
#     # mock_pdf_content = b"%PDF-1.4\n1 0 obj\n<< /Type /Page >>\nstream\nHello World\nendstream\nendobj\ntrailer\n<< /Root 1 0 R >>\n%%EOF"


#     # Wrap the content in BytesIO
#     # pdf_file = BytesIO(mock_pdf_content)

#     pdf = FPDF()
#     pdf.add_page()
#     pdf.set_font("Arial", size=12)
#     pdf.cell(200, 10, txt="Hello World", ln=True)
#     pdf_file = BytesIO()
#     pdf.output(pdf_file)
#     pdf_file.seek(0)
    
#     # Call the method
#     extracted_text = doc_ingestion_service.extract_text_from_pdf(pdf_file)
    
#     # Assert the extracted text
#     assert "Hello World" in extracted_text


#     # minimal_pdf = (
#     #     b"%PDF-1.4\n"
#     #     b"1 0 obj\n"
#     #     b"<< /Type /Catalog /Pages 2 0 R >>\n"
#     #     b"endobj\n"
#     #     b"2 0 obj\n"
#     #     b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>\n"
#     #     b"endobj\n"
#     #     b"3 0 obj\n"
#     #     b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 300 144] "
#     #     b"/Contents 4 0 R /Resources << >> >>\n"
#     #     b"endobj\n"
#     #     b"4 0 obj\n"
#     #     b"<< /Length 44 >>\n"
#     #     b"stream\n"
#     #     b"BT /F1 18 Tf 100 100 Td (Hello World) Tj ET\n"
#     #     b"endstream\n"
#     #     b"endobj\n"
#     #     b"xref\n"
#     #     b"0 5\n"
#     #     b"0000000000 65535 f \n"
#     #     b"0000000010 00000 n \n"
#     #     b"0000000053 00000 n \n"
#     #     b"0000000101 00000 n \n"
#     #     b"0000000202 00000 n \n"
#     #     b"trailer\n"
#     #     b"<< /Size 5 /Root 1 0 R >>\n"
#     #     b"startxref\n"
#     #     b"300\n"
#     #     b"%%EOF"
#     # )

#     # pdf_file = BytesIO(minimal_pdf)
#     # extracted_text = doc_ingestion_service.extract_text_from_pdf(pdf_file)
#     # assert "Hello World" in extracted_text

# def test_split_text(doc_ingestion_service):
#     """
#     Test splitting text into chunks.
#     """
#     # Mock text
#     mock_text = "This is a test sentence. Another test sentence. Yet another sentence."

#     # Call the method
#     chunks = doc_ingestion_service.split_text(mock_text, chunk_size=20)

#     # Assert the number of chunks
#     assert len(chunks) == 3
#     assert chunks[0] == "This is a test sentence."
#     assert chunks[1] == "Another test sentence."
#     assert chunks[2] == "Yet another sentence."

# def test_generate_embeddings(doc_ingestion_service):
#     """
#     Test embedding generation for text chunks.
#     """
#     # Mock text chunks
#     mock_chunks = ["This is a test sentence.", "Another test sentence."]

#     # Mock embedding model
#     doc_ingestion_service.embedding_model.encode = MagicMock(return_value=[[0.1, 0.2], [0.3, 0.4]])

#     # Call the method
#     embeddings = doc_ingestion_service.generate_embeddings(mock_chunks)

#     # Assert the embeddings
#     assert len(embeddings) == 2
#     assert embeddings[0] == [0.1, 0.2]
#     assert embeddings[1] == [0.3, 0.4]

# def test_ingest_document(doc_ingestion_service, mock_chroma_service):
#     """
#     Test the full document ingestion process.
#     """
#     # Mock file content and filename
#     mock_file_content = b"Mock PDF content"
#     mock_filename = "test.pdf"

#     # Mock methods
#     doc_ingestion_service.extract_text_from_pdf = MagicMock(return_value="This is a test sentence. Another test sentence.")
#     doc_ingestion_service.split_text = MagicMock(return_value=["This is a test sentence.", "Another test sentence."])
#     doc_ingestion_service.generate_embeddings = MagicMock(return_value=[[0.1, 0.2], [0.3, 0.4]])

#     # Call the method
#     doc_ingestion_service.ingest_document(file_content=mock_file_content, filename=mock_filename)

#     # Assert that add_document was called
#     mock_chroma_service.add_document.assert_called_once_with(
#         content=["This is a test sentence.", "Another test sentence."],
#         filenames=["test.pdf", "test.pdf"],
#         embedding=[[0.1, 0.2], [0.3, 0.4]]
#     )