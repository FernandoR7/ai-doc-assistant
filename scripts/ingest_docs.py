import argparse
import logging
import sys
from pathlib import Path
from shutil import rmtree

from langchain_chroma import Chroma
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.embeddings import get_embeddings

DOCS_PATH = PROJECT_ROOT / "data" / "docs"
CHROMA_PATH = PROJECT_ROOT / "chroma_db"
LOGGER = logging.getLogger("ingest")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Indexa documentos locais no ChromaDB."
    )
    parser.add_argument(
        "--docs-path",
        default=str(DOCS_PATH),
        help="Pasta com os documentos de entrada."
    )
    parser.add_argument(
        "--chroma-path",
        default=str(CHROMA_PATH),
        help="Pasta de persistencia do ChromaDB."
    )
    parser.add_argument(
        "--glob",
        default="**/*.txt",
        help="Padrao de arquivos para ingestao."
    )
    parser.add_argument(
        "--encoding",
        default="utf-8",
        help="Encoding usado ao ler os arquivos."
    )
    parser.add_argument(
        "--chunk-size",
        type=int,
        default=500,
        help="Tamanho maximo de cada chunk."
    )
    parser.add_argument(
        "--chunk-overlap",
        type=int,
        default=50,
        help="Sobreposicao entre chunks consecutivos."
    )
    parser.add_argument(
        "--keep-db",
        action="store_true",
        help="Nao remove o banco vetorial antes de indexar."
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Exibe logs detalhados."
    )
    return parser.parse_args()


def configure_logging(debug: bool):
    level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(
        level=logging.INFO,
        format="[%(levelname)s] %(message)s"
    )
    LOGGER.setLevel(level)

    noisy_loggers = [
        "httpcore",
        "httpx",
        "huggingface_hub",
        "sentence_transformers",
        "chromadb",
        "urllib3"
    ]
    for logger_name in noisy_loggers:
        logging.getLogger(logger_name).setLevel(logging.WARNING)


def ensure_docs_path(docs_path: Path):
    if not docs_path.exists():
        raise FileNotFoundError(
            f"Pasta de documentos nao encontrada: {docs_path}"
        )
    if not docs_path.is_dir():
        raise NotADirectoryError(
            f"O caminho de documentos nao e uma pasta: {docs_path}"
        )


def list_candidate_files(docs_path: Path, pattern: str):
    files = sorted(path for path in docs_path.glob(pattern) if path.is_file())
    if not files:
        raise FileNotFoundError(
            f"Nenhum arquivo encontrado em {docs_path} com o padrao {pattern!r}"
        )
    return files


def reset_chroma(chroma_path: Path, keep_db: bool):
    if keep_db:
        LOGGER.info("Mantendo banco vetorial existente em %s", chroma_path)
        return

    if chroma_path.exists():
        LOGGER.info("Removendo banco vetorial antigo em %s", chroma_path)
        try:
            rmtree(chroma_path)
        except PermissionError as exc:
            raise RuntimeError(
                "Nao foi possivel recriar o chroma_db porque ele esta em uso. "
                "Pare o servidor antes de rodar a ingestao novamente."
            ) from exc


def load_documents(docs_path: Path, pattern: str, encoding: str):
    LOGGER.info("Carregando documentos de %s com padrao %s", docs_path, pattern)

    loader = DirectoryLoader(
        str(docs_path),
        glob=pattern,
        loader_cls=TextLoader,
        loader_kwargs={"encoding": encoding}
    )
    documents = loader.load()

    if not documents:
        raise RuntimeError("O loader retornou zero documentos.")

    LOGGER.info("Documentos carregados: %s", len(documents))
    for document in documents:
        source = document.metadata.get("source", "<sem source>")
        LOGGER.debug("Documento carregado: %s (%s chars)", source, len(document.page_content))

    return documents


def split_documents(documents, chunk_size: int, chunk_overlap: int):
    LOGGER.info(
        "Gerando chunks com chunk_size=%s e chunk_overlap=%s",
        chunk_size,
        chunk_overlap
    )

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    chunks = text_splitter.split_documents(documents)

    if not chunks:
        raise RuntimeError("A divisao em chunks retornou zero resultados.")

    LOGGER.info("Chunks gerados: %s", len(chunks))
    for index, chunk in enumerate(chunks[:5], start=1):
        source = chunk.metadata.get("source", "<sem source>")
        preview = chunk.page_content[:100].replace("\n", " ")
        LOGGER.debug("Chunk %s de %s: %s", index, source, preview)

    return chunks


def persist_chunks(chunks, chroma_path: Path):
    LOGGER.info("Inicializando embeddings")
    embeddings = get_embeddings()

    LOGGER.info("Persistindo chunks em %s", chroma_path)
    Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=str(chroma_path)
    )


def main():
    args = parse_args()
    configure_logging(args.debug)

    docs_path = Path(args.docs_path).resolve()
    chroma_path = Path(args.chroma_path).resolve()

    try:
        LOGGER.info("Inicio da ingestao")
        LOGGER.debug("PROJECT_ROOT=%s", PROJECT_ROOT)
        LOGGER.debug("DOCS_PATH=%s", docs_path)
        LOGGER.debug("CHROMA_PATH=%s", chroma_path)

        ensure_docs_path(docs_path)
        candidate_files = list_candidate_files(docs_path, args.glob)
        LOGGER.info("Arquivos candidatos: %s", len(candidate_files))
        for file_path in candidate_files:
            LOGGER.debug("Arquivo candidato: %s", file_path)

        reset_chroma(chroma_path, args.keep_db)
        documents = load_documents(docs_path, args.glob, args.encoding)
        chunks = split_documents(
            documents,
            chunk_size=args.chunk_size,
            chunk_overlap=args.chunk_overlap
        )
        persist_chunks(chunks, chroma_path)

        LOGGER.info("Ingestao concluida com sucesso")
        print(f"{len(chunks)} chunks salvos no ChromaDB com sucesso!")
    except Exception as exc:
        LOGGER.exception("Falha na ingestao: %s", exc)
        raise SystemExit(1) from exc


if __name__ == "__main__":
    main()
