# AI Doc Assistant

<div align="center">

[![python](https://img.shields.io/badge/python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![fastapi](https://img.shields.io/badge/fastapi-api-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![langchain](https://img.shields.io/badge/langchain-rag-1C3C3C?style=flat-square)](https://www.langchain.com/)
[![chromadb](https://img.shields.io/badge/chromadb-vector_store-ff6b35?style=flat-square)](https://www.trychroma.com/)
[![license](https://img.shields.io/badge/license-MIT-blue?style=flat-square)](./LICENSE)

</div>

<div align="center">
  <h3>Local RAG assistant for querying TXT, Markdown, and PDF documents through a FastAPI API.</h3>
</div>

---

## Quick Links

- [Introduction](#introduction)
- [Features](#features)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Observability](#observability)
- [Documentation](#documentation)
- [Roadmap](#roadmap)

## Introduction

AI Doc Assistant is a portfolio project focused on building a local Retrieval-Augmented Generation pipeline with clear architecture and practical debugging support.

The application indexes documents stored in `data/docs`, transforms them into embeddings, persists them in ChromaDB, retrieves the most relevant chunks for a user question, and generates a final answer through a FastAPI API.

### Why this project matters

- It demonstrates a complete RAG workflow instead of a toy endpoint.
- It supports multiple document formats: `.txt`, `.md`, and `.pdf`.
- It was organized to be easy to inspect, debug, and evolve.
- It includes technical, non-technical, and didactic documentation.

## Features

| Feature | Description |
| --- | --- |
| Multi-format ingestion | Indexes `.txt`, `.md`, and `.pdf` documents from `data/docs`. |
| Local vector search | Uses sentence-transformer embeddings with ChromaDB for similarity retrieval. |
| API interface | Exposes a FastAPI app with `/health` and `/ask` endpoints. |
| End-to-end logging | Tracks ingestion, retrieval, prompt construction, generation, and request timing. |
| Configurable ingestion | Supports custom patterns, chunk size, overlap, and database reset control. |
| Portfolio-ready docs | Includes README plus technical, beginner-friendly, and didactic explanations. |

## Architecture

```text
Documents (.txt, .md, .pdf)
        |
        v
Ingestion + Chunking
        |
        v
Embeddings
        |
        v
ChromaDB
        |
        v
Retriever
        |
        v
Prompt + Context
        |
        v
Local LLM
        |
        v
FastAPI Response
```

## Project Structure

```text
AI project/
|-- app/
|   |-- embeddings.py
|   |-- logging_config.py
|   |-- main.py
|   |-- model.py
|   |-- rag_chain.py
|   `-- vector_store.py
|-- data/
|   `-- docs/
|       |-- fastapi.txt
|       |-- langchain.txt
|       |-- rag_notes.md
|       `-- rag_reference.pdf
|-- docs/
|   |-- rag_didatico_exemplos.md
|   |-- rag_para_leigos.md
|   `-- rag_tecnico.md
|-- scripts/
|   `-- ingest_docs.py
|-- requirements.txt
`-- README.md
```

## Getting Started

### Prerequisites

| Requirement | Version / Notes |
| --- | --- |
| Python | 3.11+ recommended |
| OS | Tested on Windows PowerShell |
| Dependencies | Installed from `requirements.txt` |

### Installation

1. Clone the repository:

```powershell
git clone https://github.com/FernandoR7/ai-doc-assistant.git
cd ai-doc-assistant
```

2. Create and activate a virtual environment:

```powershell
python -m venv .venv
& .\.venv\Scripts\Activate.ps1
```

3. Install dependencies:

```powershell
pip install -r requirements.txt
```

## Usage

### 1. Add your documents

Place supported files inside `data/docs`:

- `notes.txt`
- `guide.md`
- `manual.pdf`

### 2. Index the knowledge base

Run the ingestion script:

```powershell
python scripts/ingest_docs.py --debug
```

Default file patterns:

```text
**/*.txt
**/*.md
**/*.pdf
```

Optional custom filtering:

```powershell
python scripts/ingest_docs.py --patterns **/*.md **/*.pdf --debug
```

### 3. Start the API

```powershell
$env:APP_DEBUG='1'
python -m uvicorn app.main:app --reload
```

### 4. Open Swagger UI

```text
http://127.0.0.1:8000/docs
```

## API Endpoints

### `GET /health`

Basic health check:

```json
{
  "status": "ok"
}
```

### `POST /ask`

Request body:

```json
{
  "question": "What is FastAPI?"
}
```

Example response:

```json
{
  "answer": "FastAPI e um framework moderno para construcao de APIs com Python."
}
```

## Observability

This project was intentionally instrumented to make the full RAG flow visible.

### Ingestion logs include

- matched files per pattern
- loaded documents per format
- chunk counts
- persistence target path
- common failures such as missing folders, blocked database files, and loader issues

### Application logs include

- FastAPI startup
- LLM initialization
- retriever setup
- retrieved document previews
- prompt preview and size
- generation output preview
- HTTP request duration

Enable verbose application logs with:

```powershell
$env:APP_DEBUG='1'
```

## Supported Document Types

| Format | Loader | Notes |
| --- | --- | --- |
| `.txt` | `TextLoader` | Loaded as UTF-8 text by default |
| `.md` | `TextLoader` | Markdown is indexed as plain text content |
| `.pdf` | `PyPDFLoader` | Extracted text is indexed page-by-page before chunking |

## Documentation

Additional project guides are available in `docs/`:

- `docs/rag_tecnico.md`
- `docs/rag_para_leigos.md`
- `docs/rag_didatico_exemplos.md`

## Roadmap

- Return source documents in the API response for traceability
- Add OCR support for scanned PDFs
- Improve Portuguese generation quality with a stronger local model
- Add automated tests for ingestion and API behavior
- Move runtime settings to environment variables

## License

This project is available under the MIT License.
