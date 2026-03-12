# AI Doc Assistant

<div align="center">

[![python](https://img.shields.io/badge/python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![fastapi](https://img.shields.io/badge/fastapi-api-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![langchain](https://img.shields.io/badge/langchain-rag-1C3C3C?style=flat-square)](https://www.langchain.com/)
[![chromadb](https://img.shields.io/badge/chromadb-vector_store-ff6b35?style=flat-square)](https://www.trychroma.com/)
[![license](https://img.shields.io/badge/license-MIT-blue?style=flat-square)](./LICENSE)

</div>

<div align="center">
  <h3>Assistente RAG local para consultar documentos TXT, Markdown e PDF por meio de uma API FastAPI.</h3>
</div>

---

## Links Rápidos

- [Introdução](#introdução)
- [Funcionalidades](#funcionalidades)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Como Executar](#como-executar)
- [Uso](#uso)
- [Endpoints da API](#endpoints-da-api)
- [Observabilidade](#observabilidade)
- [Documentação](#documentação)
- [Roadmap](#roadmap)

## Introdução

AI Doc Assistant é um projeto de portfólio focado em construir um pipeline local de Retrieval-Augmented Generation com arquitetura clara e suporte prático para debug.

A aplicação indexa documentos armazenados em `data/docs`, transforma o conteúdo em embeddings, persiste os vetores no ChromaDB, recupera os chunks mais relevantes para uma pergunta do usuário e gera uma resposta final por meio de uma API FastAPI.

### Por que este projeto importa

- Demonstra um fluxo completo de RAG em vez de um endpoint de exemplo.
- Suporta múltiplos formatos de documento: `.txt`, `.md` e `.pdf`.
- Foi organizado para ser fácil de inspecionar, depurar e evoluir.
- Inclui documentação técnica, explicação para leigos e explicação didática.

## Funcionalidades

| Funcionalidade | Descrição |
| --- | --- |
| Ingestão multi-formato | Indexa documentos `.txt`, `.md` e `.pdf` a partir de `data/docs`. |
| Busca vetorial local | Usa embeddings com `sentence-transformers` e ChromaDB para recuperação semântica. |
| Interface por API | Expõe uma aplicação FastAPI com endpoints `/health` e `/ask`. |
| Logs de ponta a ponta | Rastreia ingestão, retrieval, montagem de prompt, geração e tempo da request. |
| Ingestão configurável | Permite ajustar padrões de arquivo, chunk size, overlap e controle do banco vetorial. |
| Documentação de portfólio | Inclui README e guias técnico, leigo e didático. |

## Arquitetura

```text
Documentos (.txt, .md, .pdf)
        |
        v
Ingestão + Chunking
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
Prompt + Contexto
        |
        v
LLM local
        |
        v
Resposta pela API
```

## Estrutura do Projeto

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

## Como Executar

### Pré-requisitos

| Requisito | Versão / Observação |
| --- | --- |
| Python | 3.11+ recomendado |
| Sistema | Testado em Windows PowerShell |
| Dependências | Instaladas via `requirements.txt` |

### Instalação

1. Clone o repositório:

```powershell
git clone https://github.com/FernandoR7/ai-doc-assistant.git
cd ai-doc-assistant
```

2. Crie e ative um ambiente virtual:

```powershell
python -m venv .venv
& .\.venv\Scripts\Activate.ps1
```

3. Instale as dependências:

```powershell
pip install -r requirements.txt
```

## Uso

### 1. Adicione seus documentos

Coloque arquivos suportados dentro de `data/docs`:

- `notes.txt`
- `guide.md`
- `manual.pdf`

### 2. Indexe a base de conhecimento

Execute o script de ingestão:

```powershell
python scripts/ingest_docs.py --debug
```

Padrões de arquivo usados por padrão:

```text
**/*.txt
**/*.md
**/*.pdf
```

Filtrando formatos específicos:

```powershell
python scripts/ingest_docs.py --patterns **/*.md **/*.pdf --debug
```

### 3. Inicie a API

```powershell
$env:APP_DEBUG='1'
python -m uvicorn app.main:app --reload
```

### 4. Abra o Swagger UI

```text
http://127.0.0.1:8000/docs
```

## Endpoints da API

### `GET /health`

Health check básico:

```json
{
  "status": "ok"
}
```

### `POST /ask`

Corpo da request:

```json
{
  "question": "O que é FastAPI?"
}
```

Exemplo de resposta:

```json
{
  "answer": "FastAPI é um framework moderno para construção de APIs com Python."
}
```

## Observabilidade

Este projeto foi instrumentado para tornar visível o fluxo completo do RAG.

### Os logs da ingestão mostram

- arquivos encontrados por padrão
- documentos carregados por formato
- quantidade de chunks
- caminho de persistência no banco vetorial
- falhas comuns como pasta inexistente, banco bloqueado e problemas de loader

### Os logs da aplicação mostram

- inicialização do FastAPI
- carregamento do LLM
- criação do retriever
- preview dos documentos recuperados
- preview e tamanho do prompt
- preview da resposta gerada
- tempo total da request HTTP

Ative logs mais detalhados da aplicação com:

```powershell
$env:APP_DEBUG='1'
```

## Tipos de Documento Suportados

| Formato | Loader | Observações |
| --- | --- | --- |
| `.txt` | `TextLoader` | Lido como texto UTF-8 por padrão |
| `.md` | `TextLoader` | Markdown é indexado como texto puro |
| `.pdf` | `PyPDFLoader` | O texto extraído entra na base antes do chunking |

## Documentação

Guias adicionais disponíveis em `docs/`:

- `docs/rag_tecnico.md`
- `docs/rag_para_leigos.md`
- `docs/rag_didatico_exemplos.md`

## Roadmap

- Retornar documentos-fonte na resposta da API para rastreabilidade
- Adicionar suporte a OCR para PDFs escaneados
- Melhorar a qualidade de geração em português com um modelo local mais forte
- Adicionar testes automatizados para ingestão e comportamento da API
- Mover configurações para variáveis de ambiente

## Licença

Este projeto está disponível sob a licença MIT.
