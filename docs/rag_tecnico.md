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
- suportar `.txt`, `.md` e `.pdf`
- dividir o conteudo em partes menores
- gerar embeddings
- persistir tudo em `chroma_db`

Detalhes importantes:

- `.txt` e `.md` usam `TextLoader`
- `.pdf` usa `PyPDFLoader`
- a leitura dos arquivos de texto e feita em `utf-8`
- o banco vetorial e recriado a cada ingestao, a menos que `--keep-db` seja usado
- a CLI aceita `--patterns` para filtrar formatos ou pastas

### Como a ingestao foi organizada

O script foi dividido em blocos claros:

- validacao da pasta de entrada
- mapeamento dos arquivos por padrao
- reset opcional do ChromaDB
- carga dos documentos por formato
- chunking
- persistencia final

Essa separacao melhora a manutencao e facilita identificar em que etapa um erro ocorreu.

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

O fluxo principal faz a uniao de:

- modelo de linguagem
- retriever
- prompt template

Prompt atual:

- instrui o modelo a responder com base no contexto fornecido
- pede para admitir quando a resposta nao estiver no contexto

O modulo tambem foi instrumentado com logs para mostrar:

- pergunta recebida
- documentos recuperados
- preview do contexto
- tamanho do prompt
- finalizacao da pipeline

## Modelo de linguagem

Arquivo: `app/model.py`

Modelo atual:

- `google/flan-t5-base`

Foi criado um wrapper local para integrar o modelo ao LangChain sem depender do pipeline antigo do `transformers`.

Responsabilidades do wrapper:

- tokenizar o prompt
- chamar `generate()`
- decodificar a saida
- logar tamanho do prompt, quantidade de tokens e saida gerada

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
docs (.txt/.md/.pdf) -> loader por formato -> splitter -> embeddings -> ChromaDB
```

### Consulta

```text
pergunta -> embedding da pergunta -> busca no Chroma -> contexto -> LLM -> resposta
```

## Observabilidade

O projeto foi preparado para mostrar o processo inteiro no terminal.

### Na ingestao

- quantidade de arquivos por padrao
- quantidade de documentos por formato
- preview de documentos e chunks
- caminho do banco vetorial

### Na aplicacao

- subida do app
- criacao do vector store
- inicializacao do modelo
- documentos recuperados
- prompt montado
- resposta gerada
- tempo da request HTTP

## Pontos fortes

- simples de entender
- facil de testar localmente
- separacao clara entre ingestao, retrieval e resposta
- suporta multiplos formatos de documento
- tem logs suficientes para debug real

## Limitacoes atuais

- Markdown e indexado como texto puro
- PDF depende da qualidade do texto extraido
- o modelo local pode gerar texto ruim em portugues
- nao ha retorno de fontes no endpoint
- nao ha validacao automatica de qualidade da resposta

## Melhorias tecnicas recomendadas

1. Retornar `source_documents` no endpoint.
2. Adicionar suporte a OCR para PDFs escaneados.
3. Trocar o modelo por um melhor para portugues.
4. Adicionar testes para ingestao, retrieval e endpoint.
5. Separar configuracoes em variaveis de ambiente.
