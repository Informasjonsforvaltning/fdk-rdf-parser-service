"""Ingester for messages."""
import json
import logging

from fdk_rdf_parser_service.model.reasoning_report import ReasoningReport


def ingest_for_index(index_key: str, body: bytes) -> None:
    """Ingest messages."""
    try:
        report = ReasoningReport(**json.loads(body))
        logging.info(f"RabbitMQ ingesting index {index_key!r} ")
        logging.debug(f"Ingesting with report {report}")
    except Exception as err:
        logging.error(err, exc_info=True)
        logging.error(f"Exception when ingesting {index_key}")
