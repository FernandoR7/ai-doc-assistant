# RAG Didatico Com Exemplos

## Pense em uma rotina do dia

Vamos imaginar uma rotina normal:

- cafe da manha
- almoco
- jantar
- dormir

Agora imagine que alguem pergunta:

```text
O que eu costumo fazer depois do almoco?
```

Se voce tiver uma agenda organizada, a resposta fica facil.

## Como isso se parece com RAG

### 1. Os documentos sao como uma agenda

Sua agenda pode ter anotacoes assim:

```text
07:00 - cafe da manha
12:00 - almoco
13:00 - voltar ao trabalho
22:30 - dormir
```

No projeto, os documentos funcionam como essa agenda.

## 2. Dividir em chunks e como separar a agenda por blocos

Em vez de olhar o dia inteiro de uma vez, voce pode separar em blocos:

- manha
- tarde
- noite

Isso e parecido com o chunking.

Exemplo:

- chunk 1: cafe da manha e inicio da manha
- chunk 2: almoco e tarde
- chunk 3: noite e dormir

Assim fica mais facil achar so a parte relevante.

## 3. Embeddings sao como transformar sentido em posicao

Agora pense que cada anotacao da agenda ganha uma "etiqueta invisivel" baseada no significado.

Exemplo:

- "cafe da manha" fica perto de "comer cedo"
- "almoco" fica perto de "refeicao do meio do dia"
- "dormir" fica perto de "descanso da noite"

O embedding faz isso com numeros.
Ele nao guarda o texto so pela aparencia, mas pelo sentido.

## 4. Retrieval e como procurar na parte certa da agenda

Pergunta:

```text
O que vem depois do almoco?
```

O sistema nao precisa reler tudo.
Ele procura a parte mais parecida com a pergunta.

Entao encontra algo como:

```text
12:00 - almoco
13:00 - voltar ao trabalho
```

Isso e o retrieval.

## 5. Generation e montar a resposta final

Depois de encontrar o trecho certo, o modelo monta a resposta:

```text
Depois do almoco, voce volta ao trabalho.
```

Ou seja:

- a busca encontra o material
- o modelo escreve a resposta

## Exemplo completo

### Documento

```text
07:00 - cafe da manha
08:00 - estudar
12:00 - almoco
13:00 - trabalhar
19:00 - jantar
22:30 - dormir
```

### Pergunta

```text
O que acontece depois do cafe da manha?
```

### Trecho recuperado

```text
07:00 - cafe da manha
08:00 - estudar
```

### Resposta final

```text
Depois do cafe da manha, voce estuda.
```

## Outro exemplo

### Pergunta

```text
O que eu faco a noite?
```

### Trecho recuperado

```text
19:00 - jantar
22:30 - dormir
```

### Resposta final

```text
A noite voce janta e depois dorme.
```

## Onde isso aparece no projeto

- `scripts/ingest_docs.py`: prepara e indexa os textos
- `app/embeddings.py`: transforma texto em vetores
- `app/vector_store.py`: guarda e busca os vetores
- `app/rag_chain.py`: junta busca + prompt + modelo
- `app/main.py`: expoe a API

## Resumo didatico

RAG funciona como uma pessoa organizada que:

1. guarda anotacoes
2. separa essas anotacoes em partes
3. acha a parte certa quando recebe uma pergunta
4. responde usando o que encontrou

Se quiser, pense assim:

- documentos = sua agenda
- chunks = blocos da agenda
- embeddings = mapa de significado
- retrieval = achar a pagina certa
- generation = explicar a resposta em linguagem natural
