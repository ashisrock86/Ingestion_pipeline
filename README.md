# Ingestion Pipeline (RAG-Ready Content System)

A FastAPI + LangChain-based content ingestion, processing, and retrieval system with FAISS vector search and LLM-powered RAG (Groq).

---

## 🚀 What this project does

This system implements a full **end-to-end document intelligence pipeline**:

### 1. Ingestion
- Upload PDF documents via API
- Extract raw text from files

### 2. Processing
- Clean and extract text using `PyPDF`
- Chunk documents into smaller semantic segments
- Attach metadata (document_id, filename, chunk index)

### 3. Indexing
- Generate embeddings using HuggingFace models
- Store vectors in **FAISS index**

### 4. Retrieval
- Perform semantic similarity search over stored chunks
- Return most relevant document sections

### 5. RAG (Retrieval Augmented Generation)
- Retrieve relevant chunks from FAISS
- Pass context to **Groq LLM**
- Generate grounded answers based only on retrieved content

---

## 🧠 Architecture
PDF Upload
↓
Text Extraction (PyPDF)
↓
Chunking
↓
Embedding (HuggingFace)
↓
FAISS Vector Store
↓
Similarity Search
↓
Groq LLM (RAG Answer)


---

## 📡 API Surface

### Health

- `GET /` → root message
- `GET /health` → service health check

---

### Document Ingestion

- `POST /documents/upload`

Uploads a PDF file, extracts text, chunks it, and stores embeddings in FAISS.

**Response:**
```json
{
  "document_id": "abc123",
  "filename": "file.pdf",
  "chunks_indexed": 12
}

Response of the retrival:
Response:

{
  "query": "what is this document about",
  "answer": "The document describes an Analytics Engineer with experience in...",
  "sources": [
    {
      "content": "Analytics Engineer with 10+ years...",
      "metadata": {
        "filename": "resume.pdf",
        "chunk_index": 2
      }
    }
  ]
}


Tech Stack
FastAPI (backend API)
PyPDF (text extraction)
LangChain (pipeline orchestration)
HuggingFace Embeddings
FAISS (vector database)
Groq LLM (Llama 3)

