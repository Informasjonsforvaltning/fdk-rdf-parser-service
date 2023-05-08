"""Ingester for messages."""
import logging


def ingest_for_index(index_key: str, body: bytes) -> None:
    """Ingest messages."""
    try:
        logging.info(f"RabbitMQ ingesting index {index_key!r} ")

    except Exception as err:
        logging.error(err, exc_info=True)
        logging.error(f"Exception when ingesting {index_key}")
