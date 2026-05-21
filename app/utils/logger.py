import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

def create_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel("INFO")

    MAX_BYTES = 10 * 1024 * 1024
    BACKUP_COUNT = 5


    BASE_DIR = Path(__file__).parent.parent

    console_handler = logging.StreamHandler()
    file_handler = RotatingFileHandler(
        filename = f"{BASE_DIR}/logs/library_api_logs.log",
        maxBytes = MAX_BYTES,
        backupCount = BACKUP_COUNT,
    )


    console_formater = logging.Formatter(
        "%(message)s"
    )
    file_formatter = logging.Formatter(
        "Time: %(asctime)s | Level_Name: %(levelname)s | Message: %(message)s | File: %(filename)s: %(lineno)d"
    )

    console_handler.setFormatter(console_formater)
    file_handler.setFormatter(file_formatter)

    if not logger.handlers:
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)


    return logger
