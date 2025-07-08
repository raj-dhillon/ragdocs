# 🧠 RAGDocs — Document Question Answering with Local + Cloud LLMs

RAGDocs is a containerized backend service that allows users to upload documents and query them using natural language. It leverages Retrieval-Augmented Generation (RAG) techniques with support for local LLMs (via Ollama) and OpenAI.

---

## 🚀 Features

- 📁 **/upload**: Upload documents (PDFs, text, etc.)
- ❓ **/query**: Ask questions based on uploaded content
- 🧠 **LLM Switching**: Use either local models (Ollama) or OpenAI (currently needs to be manually changed in app.py)
- 🔍 **Vector Search**: Uses ChromaDB for persistent document embeddings
- 🧪 **Unit Tested**: Test suite via Pytest
- 🐳 **Dockerized**: Fully containerized with Docker and Docker Compose
- ☸️ **Kubernetes Ready**: Deployed and tested in Minikube
- 🔐 **Secure Config**: Uses Kubernetes secrets for API keys
- 📦 **Persistent Storage**: Vector DB data survives pod restarts via PVC

---

## 🛠️ Tech Stack

- **Backend**: FastAPI
- **LLMs**: Ollama (`llama3.2`) + OpenAI fallback (current default)
- **Embeddings**: `Sentence Embeddings via all-MiniLM-L6-v2` + ChromaDB
- **Containerization**: Docker, Docker Compose
- **Orchestration**: Kubernetes (Minikube)
- **CI/CD**: (Coming soon) Jenkins pipeline with build, test, and deploy
- **Testing**: Pytest

---

## 📦 Local Setup with Docker Compose

```bash
# Clone the repo
git clone https://github.com/your-username/ragdocs.git
cd ragdocs/backend

# Create .env file for your LLM API key
echo "LLM_API_KEY=your_openai_key_here" > .env

# Start the app + Ollama
docker compose up --build
```

## ☸️ Deploy to Kubernetes

```
# Start minikube and point Docker to it
minikube start
eval $(minikube docker-env)

# Build backend image for minikube
docker build -t ragdocs-backend ./backend

# Apply manifests
kubectl apply -f k8s/

# Create secret for OpenAI key
kubectl create secret generic llm-api-key --from-literal=LLM_API_KEY=your_key_here

# Access backend
minikube service ragdocs-backend

```
