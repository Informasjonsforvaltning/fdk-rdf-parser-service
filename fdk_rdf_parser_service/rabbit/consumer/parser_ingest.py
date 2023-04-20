"""Ingester for messages."""
import logging

from fdk_rdf_parser_service.config import PARSER


async def ingest_for_index(index_key: str) -> None:
    """Ingest messages."""
    try:
        parser_endpoint = PARSER["HOST"]
        logging.info(
            f"RabbitMQ ingesting index {index_key!r} "
            f"into fdk-rdf-parser-service: {parser_endpoint}"
        )

        # Pass message to parse instantiator
        # parse_index()
        logging.info(f"Successfully ingested {index_key}")

    except Exception as err:
        logging.error(err, exc_info=True)
        logging.error(f"Exception when ingesting {index_key}")
