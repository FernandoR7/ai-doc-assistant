# RAG Tecnico

## Visao geral

Este projeto implementa um fluxo simples de RAG (Retrieval-Augmented Generation).
O objetivo e responder perguntas usando documentos locais como contexto, em vez de depender apenas do conhecimento geral do modelo.

Fluxo de alto nivel:

1. Os arquivos em `data/docs` sao carregados.
2. O texto e dividido em chunks menores.
3. Cada chunk vira um embedding vetorial.
4. Os embeddings sao salvos no ChromaDB.
5. Quando chega uma pergunta, o sistema busca os chunks mais proximos.
6. O modelo recebe pergunta + contexto recuperado e gera a resposta.

## Componentes do projeto

### Ingestao

Arquivo: `scripts/ingest_docs.py`

Responsabilidades:

- carregar os arquivos de `data/docs`
- dividir o conteudo em partes menores
- gerar embeddings
- persistir tudo em `chroma_db`

Detalhes importantes:

- o loader esta configurado para ler `.txt`
- a leitura e feita em `utf-8`
- o banco vetorial e recriado a cada ingestao

## Embeddings

Arquivo: `app/embeddings.py`

Modelo usado:

- `sentence-transformers/all-MiniLM-L6-v2`

Funcao:

- transformar texto em vetores numericos

Esses vetores permitem medir similaridade semantica. Em termos praticos, textos com significado parecido tendem a ficar proximos no espaco vetorial.

## Vector store

Arquivo: `app/vector_store.py`

Banco usado:

- ChromaDB

Funcao:

- armazenar embeddings
- recuperar os trechos mais relevantes para uma pergunta

O retriever esta configurado com `k=3`, entao ele tenta retornar os 3 chunks mais relevantes.

## Cadeia RAG

Arquivo: `app/rag_chain.py`

O chain faz a uniao de:

- modelo de linguagem
- retriever
- prompt template

Prompt atual:

- instrui o modelo a responder com base no contexto fornecido
- pede para admitir quando a resposta nao estiver no contexto

Esse ponto e central: sem prompt claro, o modelo tende a improvisar mais do que deveria.

## Modelo de linguagem

Arquivo: `app/model.py`

Modelo atual:

- `google/flan-t5-base`

Foi criado um wrapper local para integrar o modelo ao LangChain sem depender do pipeline antigo do `transformers`.

Responsabilidades do wrapper:

- tokenizar o prompt
- chamar `generate()`
- decodificar a saida

## API

Arquivo: `app/main.py`

Endpoints:

- `GET /health`
- `POST /ask`

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

## Sequencia de execucao

### Indexacao

```text
docs -> loader -> splitter -> embeddings -> ChromaDB
```

### Consulta

```text
pergunta -> embedding da pergunta -> busca no Chroma -> contexto -> LLM -> resposta
```

## Pontos fortes

- simples de entender
- facil de testar localmente
- separacao clara entre ingestao, retrieval e resposta

## Limitacoes atuais

- so indexa arquivos `.txt`
- o modelo local pode gerar texto ruim em portugues
- nao ha retorno de fontes no endpoint
- nao ha validacao de qualidade da resposta

## Melhorias tecnicas recomendadas

1. Suportar `.md` e outros formatos na ingestao.
2. Retornar `source_documents` para debug.
3. Trocar o modelo por um melhor para portugues.
4. Adicionar testes para ingestao, retrieval e endpoint.
5. Separar configuracoes em variaveis de ambiente.
