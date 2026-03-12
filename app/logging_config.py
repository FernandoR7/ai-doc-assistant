import logging
import os


def _debug_enabled() -> bool:
    return os.getenv("APP_DEBUG", "").strip().lower() in {"1", "true", "yes", "on"}


def configure_logging() -> None:
    if getattr(configure_logging, "_configured", False):
        return

    level = logging.DEBUG if _debug_enabled() else logging.INFO
    logging.basicConfig(
        level=logging.INFO,
        format="[%(levelname)s] %(name)s: %(message)s"
    )

    app_logger = logging.getLogger("app")
    app_logger.setLevel(level)

    noisy_loggers = [
        "chromadb",
        "httpcore",
        "httpx",
        "huggingface_hub",
        "sentence_transformers",
        "urllib3",
        "uvicorn.access"
    ]
    for logger_name in noisy_loggers:
        logging.getLogger(logger_name).setLevel(logging.WARNING)

    configure_logging._configured = True
