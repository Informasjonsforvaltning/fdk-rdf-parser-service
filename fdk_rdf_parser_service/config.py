"""Project config."""

import logging
import sys
from asyncio import Task
from os import environ as env
from typing import Any, Dict

from aio_pika.abc import AbstractChannel, AbstractConnection, ConsumerTag
from aiohttp.web import AppKey
from confluent_kafka.schema_registry.avro import AvroSerializer
from confluent_kafka.serialization import StringSerializer
from dotenv import load_dotenv
from pythonjsonlogger import jsonlogger

# Deferred and aliased import of KafkaProducer to avoid circular imports
import fdk_rdf_parser_service.kafka.producer as KafkaProducerModule

load_dotenv()
LOGGING_LEVEL = env.get("LOGGING_LEVEL", "INFO")

try:
    RABBITMQ: Dict[str, str] = {
        "HOST": env["RABBIT_HOST"],
        "PORT": env["RABBIT_PORT"],
        "EXCHANGE": "harvests",
        "LISTENER_ROUTING_KEY": "*.reasoned",
    }
    RABBITMQ_CREDENTIALS: Dict[str, str] = {
        "USERNAME": env["RABBIT_USERNAME"],
        "PASSWORD": env["RABBIT_PASSWORD"],
    }
    KAFKA: Dict[str, str] = {
        "SERVER": env["KAFKA_BOOTSTRAP_SERVERS"],
        "SCHEMA_REGISTRY": env["KAFKA_SCHEMA_REGISTRY"],
        "SCHEMA_PATH": "./kafka/schemas/no.fdk.rdf.parse.RdfParseEvent.avsc",
        "TOPIC": "rdf-parse-events",
    }
    REASONING_HOST = env["REASONING_HOST"]
    RESOURCE_SERVICE_HOST = env["RESOURCE_SERVICE_HOST"]
    RESOURCE_SERVICE_API_KEY = env["RESOURCE_SERVICE_API_KEY"]
except KeyError as err:
    logging.error(f"Missing environment variable: {err}")
    raise

kafka_producer_key = AppKey("kafka_producer_key", KafkaProducerModule.AIOProducer)
avro_serializer_key: AppKey[AvroSerializer] = AppKey(
    "avro_serializer_key", AvroSerializer
)
string_serializer_key: AppKey[StringSerializer] = AppKey(
    "string_serializer_key", StringSerializer
)

rabbit_connection_key = AppKey("rabbit_connection_key", AbstractConnection)
rabbit_listen_channel_key = AppKey("rabbit_listen_channel_key", AbstractChannel)
rabbit_listener_key = AppKey("rabbit_listener_key", Task[ConsumerTag])


def rabbit_connection_string() -> str:
    """String used to connect to Rabbit MQ."""
    return (
        f"amqp://{RABBITMQ_CREDENTIALS['USERNAME']}"
        f":{RABBITMQ_CREDENTIALS['PASSWORD']}"
        f"@{RABBITMQ['HOST']}"
        f":{RABBITMQ['PORT']}"
    )


def kafka_config() -> Dict[str, str]:
    """String used to connect to Kafka."""
    return {"bootstrap.servers": KAFKA["SERVER"]}


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
