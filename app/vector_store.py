import logging
from functools import lru_cache
from pathlib import Path

from langchain_chroma import Chroma
from app.embeddings import get_embeddings

CHROMA_PATH = Path(__file__).resolve().parents[1] / "chroma_db"
LOGGER = logging.getLogger("app.vector_store")


@lru_cache(maxsize=1)
def get_vector_store():
    LOGGER.info("Abrindo vector store em %s", CHROMA_PATH)
    embeddings = get_embeddings()

    vector_store = Chroma(
        persist_directory=str(CHROMA_PATH),
        embedding_function=embeddings
    )

    LOGGER.debug("Vector store inicializado")
    return vector_store


@lru_cache(maxsize=1)
def get_retriever():
    LOGGER.info("Criando retriever com k=3")
    vector_store = get_vector_store()
    retriever = vector_store.as_retriever(search_kwargs={"k": 3})
    LOGGER.debug("Retriever pronto")
    return retriever
