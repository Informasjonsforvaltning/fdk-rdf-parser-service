"""Ingester for messages."""
import logging


def ingest_for_index(index_key: str) -> None:
    """Ingest messages."""
    try:
        logging.info(f"RabbitMQ ingesting index {index_key!r} ")

        # Pass message to parse instantiator
        # parse_index()
        logging.info(f"Successfully ingested {index_key}")

    except Exception as err:
        logging.error(err, exc_info=True)
        logging.error(f"Exception when ingesting {index_key}")
