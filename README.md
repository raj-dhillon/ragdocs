# 🚀 Project: RAGDocs

An AI-powered document QA service that allows you to upload documents and ask questions based on their content. Built with FastAPI, ChromaDB, and a locally hosted LLM, this project is designed for scalability and reliability, leveraging Kubernetes for deployment and Jenkins for CI/CD automation.

---

## 🔧 **What It Does**

- **Upload Documents**: Supports various formats like PDFs, Markdown, and DOCX.
- **Question Answering**: Uses a locally hosted LLM to answer questions based on the uploaded documents.
- **Document Storage**: Stores document content and metadata in ChromaDB for efficient querying.
- **Automated Testing**: Includes unit tests to ensure reliability.
- **CI/CD Pipeline**: Managed via Jenkins for automated builds, testing, and deployment.
- **Kubernetes Deployment**: Scales seamlessly with containerized infrastructure.

---

## 🛠️ **Tech Stack**

- **Backend**: FastAPI
- **Database**: ChromaDB (DuckDB + Parquet for persistence)
- **LLM**: Locally hosted language model (e.g., Ollama or similar)
- **Containerization**: Docker
- **Orchestration**: Kubernetes
- **CI/CD**: Jenkins
- **Testing**: Pytest

---
