"""Logger module for the API"""

import logging
import os

from ..common.config import LoggingConfig
from ..utils.colorama import Fore, Style


class ColoredFormatter(logging.Formatter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Define color codes
        self.colors = {
            "DEBUG": Fore.CYAN,
            "INFO": Fore.GREEN,
            "WARNING": Fore.YELLOW,
            "ERROR": Fore.RED,
            "CRITICAL": Fore.MAGENTA + Style.BRIGHT,
        }

    def format(self, record):
        # Apply color to the entire log message
        message = super().format(record)
        return f"{self.colors.get(record.levelname, Fore.WHITE + Style.BRIGHT)}{message}{Style.RESET_ALL}"


class CustomLogger(logging.Logger):
    def __init__(
        self, name: str, logging_config: LoggingConfig = LoggingConfig()
    ) -> None:
        super().__init__(name=name, level=logging_config.logger_level)
        formatter = ColoredFormatter(logging_config.logging_format)

        console = logging.StreamHandler()
        console.setLevel(logging_config.console_log_level)
        console.setFormatter(formatter)

        if (
            logging_config.file_log_name is not None
            and logging_config.file_log_level is not None
        ):
            if not os.path.exists(os.path.dirname(logging_config.file_log_name)):
                os.makedirs(os.path.dirname(logging_config.file_log_name))
            file_handler = logging.FileHandler(
                filename=logging_config.file_log_name,
                mode="a",
                encoding="utf-8",
            )
            file_handler.setLevel(logging_config.file_log_level)
            file_handler.setFormatter(formatter)
            self.addHandler(file_handler)

        self.addHandler(console)


class ApiLogger(CustomLogger):
    _instances: dict[str, "ApiLogger"] = {}

    def __new__(
        cls, name: str, logging_config: LoggingConfig = LoggingConfig()
    ) -> "ApiLogger":
        """Singleton pattern for ApiLogger class"""
        if name not in cls._instances:
            cls._instances[name] = super().__new__(cls)
        return cls._instances[name]

    def __init__(
        self, name: str, logging_config: LoggingConfig = LoggingConfig()
    ) -> None:
        super().__init__(name=name, logging_config=logging_config)

    @classmethod
    def cinfo(cls, msg: str, *args, **kwargs) -> None:
        if cls.__name__ not in cls._instances:
            cls(cls.__name__)
        super(ApiLogger, cls._instances[cls.__name__]).info(msg, *args, **kwargs)

    @classmethod
    def cdebug(cls, msg: str, *args, **kwargs) -> None:
        if cls.__name__ not in cls._instances:
            cls(cls.__name__)
        super(ApiLogger, cls._instances[cls.__name__]).debug(msg, *args, **kwargs)

    @classmethod
    def cwarning(cls, msg: str, *args, **kwargs) -> None:
        if cls.__name__ not in cls._instances:
            cls(cls.__name__)
        super(ApiLogger, cls._instances[cls.__name__]).warning(msg, *args, **kwargs)

    @classmethod
    def cerror(cls, msg: str, *args, **kwargs) -> None:
        if cls.__name__ not in cls._instances:
            cls(cls.__name__)
        super(ApiLogger, cls._instances[cls.__name__]).error(msg, *args, **kwargs)

    @classmethod
    def cexception(cls, msg: str, *args, **kwargs) -> None:
        if cls.__name__ not in cls._instances:
            cls(cls.__name__)
        super(ApiLogger, cls._instances[cls.__name__]).exception(msg, *args, **kwargs)

    @classmethod
    def ccritical(cls, msg: str, *args, **kwargs) -> None:
        if cls.__name__ not in cls._instances:
            cls(cls.__name__)
        super(ApiLogger, cls._instances[cls.__name__]).critical(msg, *args, **kwargs)

    @classmethod
    def clog(cls, level: int, msg: str, *args, **kwargs) -> None:
        if cls.__name__ not in cls._instances:
            cls(cls.__name__)
        super(ApiLogger, cls._instances[cls.__name__]).log(level, msg, *args, **kwargs)


if __name__ == "__main__":
    ApiLogger.cdebug("Testing logger: debug")
    ApiLogger.cinfo("Testing logger: info")
    ApiLogger.cwarning("Testing logger: warning")
    try:
        raise Exception("Test exception")
    except Exception:
        ApiLogger.cerror("Testing logger: error", exc_info=True)
    ApiLogger.ccritical("Testing logger: critical")
ApiLogger.cinfo
