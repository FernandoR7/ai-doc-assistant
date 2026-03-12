import logging
from time import perf_counter

from fastapi import FastAPI, Request
from pydantic import BaseModel

from app.logging_config import configure_logging

configure_logging()

from app.rag_chain import get_rag_chain

LOGGER = logging.getLogger("app.main")

app = FastAPI(title="AI Doc Assistant")

LOGGER.info("Inicializando aplicacao FastAPI")
rag_chain = get_rag_chain()
LOGGER.info("RAG chain pronta")


class QuestionRequest(BaseModel):
    question: str


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = perf_counter()
    LOGGER.info("HTTP %s %s", request.method, request.url.path)
    response = await call_next(request)
    duration_ms = (perf_counter() - start) * 1000
    LOGGER.info(
        "HTTP %s %s -> %s em %.2f ms",
        request.method,
        request.url.path,
        response.status_code,
        duration_ms
    )
    return response


@app.get("/health")
def health_check():
    LOGGER.debug("Health check chamado")
    return {"status": "ok"}


@app.post("/ask")
def ask_question(request: QuestionRequest):
    LOGGER.info("Recebida pergunta no endpoint /ask")
    LOGGER.debug("Payload recebido: %s", request.question)
    response = rag_chain.invoke({"query": request.question})
    LOGGER.info("Resposta enviada pelo endpoint /ask")
    return {"answer": response["result"]}
