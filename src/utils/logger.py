import logging
from pathlib import Path


class Logger:

    @staticmethod
    def get_logger(name: str):

        log_directory = Path(__file__).resolve().parents[2] / "data" / "logs"
        log_directory.mkdir(parents=True, exist_ok=True)

        logger = logging.getLogger(name)

        if logger.handlers:
            return logger

        logger.setLevel(logging.INFO)

        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(message)s"
        )

        file_handler = logging.FileHandler(
            log_directory / "pipeline.log",
            encoding="utf-8"
        )

        file_handler.setFormatter(formatter)

        console_handler = logging.StreamHandler()

        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)

        logger.addHandler(console_handler)

        return logger
