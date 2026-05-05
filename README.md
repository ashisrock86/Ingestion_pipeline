# Ingestion Pipeline

A FastAPI-based content ingestion and retrieval prototype.

## What is included

- `app/api/main.py` - FastAPI app entrypoint with a runnable `main()` function.
- `app/api/routes/health.py` - health check endpoint.
- `app/api/routes/documents.py` - document upload endpoint.
- `pyproject.toml` - project metadata and dependencies.

## Current API surface

- `GET /` - root welcome endpoint.
- `GET /health` - simple health check.
- `POST /documents/upload` - upload a raw document file and receive file metadata.

## How to run

1. Activate your Python environment:
   ```bash
   source .venv/bin/activate
   ```
2. Start the app:
   ```bash
   python app/api/main.py
   ```
3. Alternatively run Uvicorn directly:
   ```bash
   uvicorn app.api.main:app --reload --port 8200
   ```

## Development progress so far

- Built a minimal FastAPI-first application scaffold.
- Added a file upload endpoint in `app/api/routes/documents.py`.
- Added a health endpoint in `app/api/routes/health.py`.
- Configured the API router and app entrypoint in `app/api/main.py`.

## Architecture and next steps

This project is intended to become a content pipeline with:

- ingestion of raw content,
- processing to structured form,
- retrieval via index/query,
- traceability of transformations.

Next development steps include:

- wire in a relational database for raw and processed storage,
- implement document processing/cleaning/summarization,
- add retrieval/search endpoints,
- add traceability metadata and chunk indexing,
- build a simple frontend or admin UI for browsing ingested documents.

## Notes

At this stage, the upload endpoint returns only file metadata and size. The current app includes a placeholder for DB state in `app/api/main.py`.
