"""Project config."""

import logging
import multiprocessing
import sys
from os import environ as env
from typing import Any

from dotenv import load_dotenv
from pythonjsonlogger import jsonlogger

load_dotenv()
LOG_LEVEL = env.get("LOG_LEVEL", "INFO")

HOST_PORT = env.get("HOST_PORT", "8080")

# Gunicorn config
num_cores = multiprocessing.cpu_count()
bind = f":{HOST_PORT}"
threads = 1  # 2
workers = 1  # max((2 * num_cores) + 1, 12)
loglevel = str(LOG_LEVEL)
accesslog = "-"


def init_logger(name: str) -> logging.Logger:
    """Initiate logger."""
    logger = logging.getLogger(name)
    logger.setLevel(str(LOG_LEVEL))
    log_handler = logging.StreamHandler(sys.stdout)
    log_handler.setFormatter(StackdriverJsonFormatter())
    log_handler.addFilter(PingFilter())
    log_handler.addFilter(ReadyFilter())
    log_handler.addFilter(BlackboxExporterFilter())
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
        """Init json-logger."""
        jsonlogger.JsonFormatter.__init__(self, *args, **kwargs, fmt=fmt)

    def process_log_record(self: Any, log_record: Any) -> Any:
        """Process log record to a json-format compatible with Stackdriver."""
        log_record["severity"] = log_record["levelname"]
        del log_record["levelname"]
        log_record["serviceContext"] = {"service": "fdk-rdf-parser-service"}
        return super(StackdriverJsonFormatter, self).process_log_record(log_record)


# Override the logger to remove healthcheck (ping) from the access log and format logs as json
class CustomGunicornLogger(glogging.Logger):
    """Custom Gunicorn Logger class."""

    def setup(self: Any, cfg: Any) -> None:
        """Set up function."""
        super().setup(cfg)

        access_logger = logging.getLogger("gunicorn.access")
        access_logger.addFilter(PingFilter())
        access_logger.addFilter(ReadyFilter())
        access_logger.addFilter(BlackboxExporterFilter())

        root_logger = logging.getLogger()
        root_logger.setLevel(loglevel)

        other_loggers = [
            "gunicorn",
            "gunicorn.error",
            "gunicorn.http",
            "gunicorn.http.wsgi",
        ]
        loggers = [logging.getLogger(name) for name in other_loggers]
        loggers.append(root_logger)
        loggers.append(access_logger)

        json_handler = logging.StreamHandler(sys.stdout)
        json_handler.setFormatter(StackdriverJsonFormatter())

        for logger in loggers:
            for handler in logger.handlers:
                logger.removeHandler(handler)
            logger.addHandler(json_handler)


class PingFilter(logging.Filter):
    """Custom Ping Filter class."""

    def filter(self: Any, record: logging.LogRecord) -> bool:
        """Filter function."""
        return "GET /ping" not in record.getMessage()


class ReadyFilter(logging.Filter):
    """Custom Ready Filter class."""

    def filter(self: Any, record: logging.LogRecord) -> bool:
        """Filter function."""
        return "GET /ready" not in record.getMessage()


class BlackboxExporterFilter(logging.Filter):
    """Custom Blackbox Exporter Filter class."""

    def filter(self: Any, record: logging.LogRecord) -> bool:
        """Filter function."""
        return "Blackbox Exporter" not in record.getMessage()


logger_class = CustomGunicornLogger
