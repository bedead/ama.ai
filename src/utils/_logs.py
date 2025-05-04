import logging
import os
from typing import Optional

logger: logging.Logger = logging.getLogger("ama")


def _basic_config() -> None:
    # e.g. [2023-10-05 14:12:26 - ama.groq:818 - DEBUG] HTTP Request: POST http://127.0.0.1:4010/foo/bar "200 OK"
    logging.basicConfig(
        format="[%(asctime)s - %(name)s:%(lineno)d - %(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        encoding="utf-8",
    )


def setup_logging(
    log_type: Optional[str] = None, log_file: Optional[str] = None
) -> None:
    env = log_type or os.environ.get("LOG_TYPE")
    print(f"env: {env}")
    file_path = log_file or os.environ.get("LOG_FILE_PATH", "ama.log")
    _basic_config()

    if env == "debug":
        logger.setLevel(logging.DEBUG)
        # create file handler which logs even debug messages
        fh = logging.FileHandler(filename=file_path)
        fh.setLevel(logging.DEBUG)

        # create console handler with a higher log level
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
    elif env == "info":
        logger.setLevel(logging.INFO)
        fh = logging.FileHandler(filename=file_path)
        fh.setLevel(logging.DEBUG)

        # create console handler with a higher log level
        ch = logging.StreamHandler()
        ch.setLevel(logging.WARNING)

    logger.addHandler(fh)
    logger.addHandler(ch)
