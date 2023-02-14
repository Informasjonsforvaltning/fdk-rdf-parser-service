"""Gunicorn module for fdk-rdf-parser-service."""
import logging
import multiprocessing
import sys
from typing import Any

from gunicorn import glogging
from pythonjsonlogger import jsonlogger

from fdk_rdf_parser_service.config import HOST_PORT, LOGGING_LEVEL

# Gunicorn config
bind = ":" + HOST_PORT
workers = multiprocessing.cpu_count() * 2 + 1
threads = 2 * multiprocessing.cpu_count()
loglevel = str(LOGGING_LEVEL)
accesslog = "-"


class StackdriverJsonFormatter(jsonlogger.JsonFormatter, object):
    """json log formatter."""

    def __init__(
        self, fmt="%(levelname) %(message)", style="%", *args, **kwargs  # noqa
    ):  # noqa
        """Instantiate the logger."""
        jsonlogger.JsonFormatter.__init__(self, fmt=fmt, *args, **kwargs)

    def process_log_record(self, log_record):  # noqa
        log_record["severity"] = log_record["levelname"]
        del log_record["levelname"]
        return super(StackdriverJsonFormatter, self).process_log_record(log_record)


# Override the logger to remove healthcheck (ping) from the access log and format logs as json
class CustomGunicornLogger(glogging.Logger):
    """Custom Gunicorn Logger class."""

    def setup(self, cfg: Any) -> None:
        """Set up function."""
        super().setup(cfg)

        access_logger = logging.getLogger("gunicorn.access")
        access_logger.addFilter(PingFilter())
        access_logger.addFilter(ReadyFilter())

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

    def filter(self, record: logging.LogRecord) -> bool:
        """Filter function."""
        return "GET /ping" not in record.getMessage()


class ReadyFilter(logging.Filter):
    """Custom Ready Filter class."""

    def filter(self, record: logging.LogRecord) -> bool:
        """Filter function."""
        return "GET /ready" not in record.getMessage()


logger_class = CustomGunicornLogger
