"""Project config."""

import logging
import sys
from os import environ as env
from typing import Any, Dict

from dotenv import load_dotenv
from pythonjsonlogger import jsonlogger

load_dotenv()
LOGGING_LEVEL = env.get("LOGGING_LEVEL", "INFO")


def init_logger() -> logging.Logger:
    """Initiate logger."""
    logger = logging.getLogger()
    logger.setLevel(str(LOGGING_LEVEL))
    log_handler = logging.StreamHandler(sys.stdout)
    log_handler.setFormatter(StackdriverJsonFormatter())
    log_handler.addFilter(PingFilter())
    log_handler.addFilter(ReadyFilter())
    logger.addHandler(log_handler)
    return logger


class StackdriverJsonFormatter(jsonlogger.JsonFormatter, object):
    """json log formatter."""

    def __init__(
        self: Any,
        fmt: str = "%(levelname) %(message)",
        style: str = "%",
        *args: Any,
        **kwargs: Any,
    ) -> None:
        jsonlogger.JsonFormatter.__init__(
            self,
            *args,
            **kwargs,
            fmt=fmt,
        )

    def process_log_record(self: Any, log_record: Dict) -> Any:
        """."""
        log_record["severity"] = log_record["levelname"]
        del log_record["levelname"]
        log_record["serviceContext"] = {"service": "fdk-rdf-parser-service"}
        return super(StackdriverJsonFormatter, self).process_log_record(log_record)


class PingFilter(logging.Filter):
    """Custom Ping Filter class."""

    def filter(self, record: logging.LogRecord) -> bool:
        """Filter function."""
        return "GET /ping" not in record.getMessage()


class ReadyFilter(logging.Filter):
    """Custom Ready Filter class."""

    def filter(self, record: logging.LogRecord) -> bool:
        """Filter function."""
        return "GET /ready" not in record.getMessage()
