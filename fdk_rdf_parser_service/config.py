"""Project config."""

import logging
from os import environ as env
import sys
from typing import Any, Dict

from dotenv import load_dotenv
from pythonjsonlogger import jsonlogger

load_dotenv()

LOGGING_LEVEL = env.get("LOGGING_LEVEL", "INFO")

HOST_PORT = env.get("HOST_PORT", "8000")

MONGO_DB: Dict[str, str] = {
    "HOST": env.get("DB_HOST", "http://localhost"),
    "PORT": env.get("DB_PORT", "27017"),
    "USERNAME": env.get("DB_USER", "admin"),
    "PASSWORD": env.get("DB_PASSWORD", "admin"),
}

RABBITMQ: Dict[str, str] = {
    "HOST": env.get("RABBIT_HOST", "http://localhost"),
    "USERNAME": env.get("RABBIT_USERNAME", "admin"),
    "PASSWORD": env.get("RABBIT_PASSWORD", "admin"),
    "TYPE": "topic",
    "EXCHANGE": "harvests",
    "LISTENER_ROUTING_KEY": "*.reasoned",
}

PARSER: Dict[str, str] = {"HOST": env.get("PARSER_HOST", "http://localhost")}


class StackdriverJsonFormatter(jsonlogger.JsonFormatter, object):
    """json log formatter."""

    def __init__(
        self: Any,
        fmt: str = "%(levelname) %(message)",
        style: str = "%",
        *args: Any,
        **kwargs: Any
    ) -> None:
        jsonlogger.JsonFormatter.__init__(self, fmt=fmt, *args, **kwargs)

    def process_log_record(self: Any, log_record: Dict) -> Any:
        """."""
        log_record["severity"] = log_record["levelname"]
        del log_record["levelname"]
        log_record["serviceContext"] = {"service": "fdk-rdf-parser-service"}
        return super(StackdriverJsonFormatter, self).process_log_record(log_record)


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
