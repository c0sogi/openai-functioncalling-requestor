import logging
from dataclasses import dataclass
from typing import Optional

from dotenv import load_dotenv

if load_dotenv():
    print("- Loaded .env file successfully.")
else:
    print("- Failed to load .env file.")


@dataclass
class LoggingConfig:
    logger_level: int = logging.DEBUG
    console_log_level: int = logging.INFO
    file_log_level: Optional[int] = logging.DEBUG
    file_log_name: Optional[str] = "./logs/debug.log"
    logging_format: str = "[%(asctime)s] %(name)s:%(levelname)s - %(message)s"


logging_config = LoggingConfig()
