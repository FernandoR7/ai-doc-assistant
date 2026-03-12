# AI Doc Assistant

Assistente de perguntas e respostas com RAG local, construído com FastAPI, LangChain, ChromaDB e modelos Hugging Face.

O projeto indexa documentos locais, recupera os trechos mais relevantes para uma pergunta e gera respostas com base nesse contexto. O foco aqui nao e so "fazer funcionar", mas deixar o fluxo observavel e depuravel de ponta a ponta.

## Destaques

- API REST com FastAPI para consulta de documentos
- pipeline de RAG local com embeddings, retrieval e geracao
- ingestao com logs detalhados e validacoes de erro
- observabilidade no fluxo inteiro: API, retriever, prompt e modelo
- documentacao em tres niveis: tecnico, leigo e didatico

## Stack

- Python
- FastAPI
- LangChain
- ChromaDB
- sentence-transformers
- Transformers
- PyTorch

## Arquitetura

```text
Documentos locais
    ->
Ingestao e chunking
    ->
Embeddings
    ->
ChromaDB
    ->
Retriever
    ->
Prompt com contexto
    ->
LLM local
    ->
Resposta via API
```

## Fluxo do projeto

### 1. Ingestao

O script `scripts/ingest_docs.py`:

- le os arquivos em `data/docs`
- divide o texto em chunks
- gera embeddings
- persiste os vetores no ChromaDB
- registra logs por etapa para facilitar debug

### 2. Retrieval

O módulo `app/vector_store.py` abre o banco vetorial e cria o retriever. Quando chega uma pergunta, o sistema busca os chunks semanticamente mais proximos.

### 3. Geracao

O módulo `app/rag_chain.py` monta o contexto recuperado, injeta esse contexto no prompt e envia o texto final para o modelo definido em `app/model.py`.

### 4. API

O endpoint `POST /ask` recebe a pergunta e devolve a resposta final.

## Estrutura

```text
app/
  embeddings.py
  logging_config.py
  main.py
  model.py
  rag_chain.py
  vector_store.py
data/
  docs/
docs/
  rag_tecnico.md
  rag_para_leigos.md
  rag_didatico_exemplos.md
scripts/
  ingest_docs.py
```

## Como executar

### 1. Criar e ativar o ambiente virtual

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

### 5. Testar

Swagger:

```text
http://127.0.0.1:8000/docs
```

Exemplo de request:

```json
{
  "question": "What is FastAPI?"
}
```

Exemplo de resposta:

```json
{
  "answer": "FastAPI e um framework moderno para construcao de APIs com Python."
}
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

## Observabilidade e debug

Este projeto foi instrumentado para facilitar acompanhamento do processo inteiro.

### Na ingestao

- arquivos encontrados
- documentos carregados
- quantidade de chunks
- persistencia no ChromaDB
- erros de caminho, encoding e banco bloqueado

### Na aplicacao

- inicializacao do app
- carregamento do modelo
- criacao do retriever
- documentos recuperados
- preview do prompt
- resposta gerada
- tempo total da request HTTP

Para ativar logs mais detalhados na API:

```powershell
$env:APP_DEBUG='1'
```

## O que este projeto demonstra

- construcao de um fluxo RAG do zero
- organizacao por responsabilidades
- integracao entre API, vector store e modelo local
- preocupacao com debuggabilidade e manutencao
- documentacao orientada a diferentes publicos

## Melhorias futuras

- suporte a Markdown e PDF na ingestao
- retorno de fontes no endpoint
- avaliacao automatica da qualidade das respostas
- troca do modelo por uma opcao mais forte em portugues
- testes automatizados para ingestao e API

## Documentacao complementar

- `docs/rag_tecnico.md`
- `docs/rag_para_leigos.md`
- `docs/rag_didatico_exemplos.md`
