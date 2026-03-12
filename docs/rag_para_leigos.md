# RAG Para Leigos

## O que este projeto faz

Este projeto e um assistente que responde perguntas lendo arquivos que voce colocou dentro da pasta de documentos.

Ele nao funciona como um "robo que sabe tudo".
Ele funciona mais como alguem que:

- procura informacao em um caderno
- encontra os trechos mais proximos do assunto
- usa esses trechos para montar uma resposta

## Que tipos de arquivo ele entende

Hoje o projeto consegue ler:

- arquivos de texto `.txt`
- arquivos de documentacao `.md`
- arquivos `.pdf`

Isso significa que voce pode montar sua base com:

- anotacoes simples
- documentacao escrita em Markdown
- apostilas e materiais em PDF

## Ideia principal

Imagine que voce tem varios papeis e arquivos com anotacoes sobre FastAPI, LangChain e outros temas.

Quando alguem faz uma pergunta, o sistema:

1. procura os trechos mais relacionados
2. junta esses trechos
3. pede ao modelo para responder usando esse material

Ou seja:

- ele primeiro procura
- depois responde

Esse "procurar antes de responder" e justamente a ideia do RAG.

## O que significa RAG

RAG = Retrieval-Augmented Generation

Em linguagem simples:

- Retrieval = buscar trechos relevantes
- Augmented = acrescentar esses trechos na pergunta
- Generation = gerar a resposta final

## Exemplo simples

Voce pergunta:

```text
O que e FastAPI?
```

O sistema vai:

- abrir sua base de documentos
- encontrar o trecho que fala de FastAPI
- mandar esse trecho para o modelo
- devolver uma resposta usando esse texto

## Como PDF e Markdown entram nisso

Se voce colocar um arquivo Markdown:

- ele sera lido como texto
- o conteudo vira parte da base

Se voce colocar um PDF:

- o sistema tenta extrair o texto das paginas
- esse texto tambem entra na base

Entao, no fim, o projeto trata tudo como conteudo consultavel.

## Por que isso e melhor do que perguntar direto ao modelo

Sem RAG:

- o modelo tenta responder do que ele "lembra"
- ele pode errar ou inventar

Com RAG:

- o modelo recebe apoio dos seus documentos
- a chance de responder dentro do contexto aumenta

## Uma comparacao facil

Sem RAG:

- e como responder uma prova so de memoria

Com RAG:

- e como responder a prova podendo consultar suas anotacoes

## O que existe dentro deste projeto

- uma pasta com documentos
- um sistema que transforma esses textos em numeros para comparacao
- um banco que guarda esses numeros
- um modelo que monta a resposta final
- uma API para voce perguntar pelo navegador ou pelo Swagger

## O que voce precisa lembrar

Se o documento estiver ruim, a resposta tende a ficar ruim.

Se o documento estiver bom, a resposta tende a melhorar.

Em outras palavras:

- lixo entra, lixo sai

Isso tambem vale para PDF:

- se o PDF tiver texto ruim ou for mal extraido, a resposta pode piorar

## Resumo final

Este projeto e um assistente que consulta seus documentos antes de responder.
Ele nao depende apenas de "memoria".
Ele busca contexto em `.txt`, `.md` e `.pdf` e tenta responder com base no que encontrou.
