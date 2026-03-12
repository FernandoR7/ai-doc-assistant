import logging
from functools import lru_cache

from langchain_huggingface import HuggingFaceEmbeddings

LOGGER = logging.getLogger("app.embeddings")


@lru_cache(maxsize=1)
def get_embeddings():
    LOGGER.info("Inicializando embeddings com sentence-transformers/all-MiniLM-L6-v2")
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    LOGGER.debug("Embeddings prontos")
    return embeddings
