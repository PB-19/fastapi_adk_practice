import os
import logging
from logging import Logger
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv
load_dotenv()

class AppLogger:
    _configured: bool = False

    @classmethod
    def _configure(cls, level: int = logging.INFO, log_file: str = os.getenv("LOG_FILE")) -> None:
        if cls._configured: return

        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        formatter = logging.Formatter(
            fmt="%(asctime)s [%(levelname)s] [%(name)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        console_handler.setLevel(level)

        # File handler
        file_handler = logging.FileHandler(log_path, encoding="utf-8")
        file_handler.setFormatter(formatter)
        file_handler.setLevel(level)

        # Root logger
        root_logger = logging.getLogger()
        root_logger.setLevel(level)
        root_logger.addHandler(console_handler)
        root_logger.addHandler(file_handler)

        cls._configured = True

    @classmethod
    def get_logger(cls, name: Optional[str] = None, level: int = logging.INFO, log_file: str = "app.log") -> Logger:
        cls._configure(level=level, log_file=log_file)
        return logging.getLogger(name)
