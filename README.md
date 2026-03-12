# AI Doc Assistant

Projeto de portfolio com RAG local usando FastAPI, LangChain, ChromaDB e modelos Hugging Face.

## O que o projeto faz

Este projeto indexa documentos locais, recupera os trechos mais relevantes para uma pergunta e usa um modelo local para responder com base nesse contexto.

Fluxo principal:

1. Ler documentos em `data/docs`
2. Dividir o texto em chunks
3. Gerar embeddings
4. Salvar no ChromaDB
5. Recuperar contexto relevante
6. Gerar resposta via API

## Stack

- FastAPI
- LangChain
- ChromaDB
- sentence-transformers
- Transformers
- PyTorch

## Estrutura

```text
app/
  embeddings.py
  logging_config.py
  main.py
  model.py
  rag_chain.py
  vector_store.py
data/docs/
docs/
scripts/
  ingest_docs.py
```

## Como rodar

### 1. Criar e ativar o ambiente

```powershell
python -m venv .venv
& .\.venv\Scripts\Activate.ps1
```

### 2. Instalar dependencias

```powershell
pip install -r requirements.txt
```

### 3. Indexar os documentos

```powershell
python scripts/ingest_docs.py --debug
```

### 4. Subir a API

```powershell
$env:APP_DEBUG='1'
python -m uvicorn app.main:app --reload
```

## Endpoints

### Health check

```http
GET /health
```

### Perguntas

```http
POST /ask
Content-Type: application/json
```

Exemplo:

```json
{
  "question": "What is FastAPI?"
}
```

## Diferenciais do projeto

- pipeline de ingestao com debug
- logs no fluxo inteiro da aplicacao
- separacao clara entre embeddings, retrieval e resposta
- documentacao em niveis tecnico, leigo e didatico

## Documentacao adicional

- `docs/rag_tecnico.md`
- `docs/rag_para_leigos.md`
- `docs/rag_didatico_exemplos.md`
