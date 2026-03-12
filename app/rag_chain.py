import logging
from dataclasses import dataclass

from langchain_classic.prompts import PromptTemplate

from app.logging_config import configure_logging
from app.model import get_llm
from app.vector_store import get_retriever

configure_logging()

LOGGER = logging.getLogger("app.rag_chain")


@dataclass
class DebuggableRAGChain:
    llm: object
    retriever: object
    prompt: PromptTemplate

    def invoke(self, inputs: dict):
        query = inputs["query"]
        LOGGER.info("Iniciando pipeline RAG")
        LOGGER.info("Pergunta recebida: %s", query)

        documents = self.retriever.invoke(query)
        LOGGER.info("Documentos recuperados: %s", len(documents))

        if not documents:
            LOGGER.warning("Nenhum documento encontrado para a pergunta")

        for index, document in enumerate(documents, start=1):
            source = document.metadata.get("source", "<sem source>")
            preview = document.page_content[:160].replace("\n", " ")
            LOGGER.debug("Documento %s de %s: %s", index, source, preview)

        context = "\n\n".join(document.page_content for document in documents)
        prompt_text = self.prompt.format(context=context, question=query)
        LOGGER.info("Prompt montado com %s caracteres", len(prompt_text))
        LOGGER.debug("Prompt final: %s", prompt_text[:800].replace("\n", " "))

        answer = self.llm.invoke(prompt_text)
        LOGGER.info("Pipeline RAG concluido")
        return {
            "query": query,
            "result": answer,
            "source_documents": documents
        }


def get_rag_chain():
    LOGGER.info("Montando pipeline RAG")
    llm = get_llm()
    retriever = get_retriever()

    prompt_template = """
    Voce e um assistente que responde perguntas com base no contexto fornecido.
    Se a resposta nao estiver no contexto, diga claramente que nao encontrou a informacao.

    Contexto:
    {context}

    Pergunta:
    {question}

    Resposta:
    """

    prompt = PromptTemplate(
        template=prompt_template,
        input_variables=["context", "question"]
    )

    LOGGER.debug("Prompt template configurado")
    return DebuggableRAGChain(
        llm=llm,
        retriever=retriever,
        prompt=prompt
    )
