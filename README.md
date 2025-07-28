# RAGgeaton – AI Retrieval Broker

RAGgeaton is a modular, FastAPI-based RAG (Retrieval-Augmented Generation) service that provides semantic search and AI chat over course-specific memory. It's designed to work with Moodle plugins, providing endpoints for ingestion and contextual chat generation using the LlamaIndex framework and ChromaDB for vector storage.

## Features

- FastAPI REST API with two endpoints:
  - `POST /ingest` – Ingest course data into memory
  - `POST /query` – Answer questions based on ingested content
- Uses LlamaIndex for chunking, embedding, and RAG
- Embeds with Sentence Transformers or OpenAI
- Stores persistent vectors in ChromaDB
- Supports Docker deployment and environment configuration

---

## 📦 Installation

### 1. Clone and Setup

```bash
git clone <your-repo-url>
cd raggeaton
python3.11 -m venv .venv
source .venv/bin/activate
```

## Project Structure

- `app/` — Application code (FastAPI server, ingestion, query, config)
- `memory/` — Original input content
- `db/` — ChromaDB vector storage

## 🚀 Quickstart

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
2. **Run the application:**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```
   The server will be available at: [http://0.0.0.0:8000](http://0.0.0.0:8000)

## ⚙️ Environment Variables

Copy the example environment file and edit as needed:
```bash
cp .env.example .env
```
Or create a `.env` file with your configuration. See `.env.example` for available options.
