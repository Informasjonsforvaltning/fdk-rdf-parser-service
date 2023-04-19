"""Ingester for messages."""
import logging

import requests

from fdk_rdf_parser_service.config import PARSER


async def ingest_for_index(index_key: str) -> None:
    """Ingest messages."""
    try:
        parser_endpoint = PARSER["HOST"]
        logging.info(
            f"RabbitMQ ingesting index {index_key!r} "
            f"into fdk-rdf-parser-service: {parser_endpoint}"
        )
        # response = requests.post(
        #     url=parser_endpoint,
        #     params={"name": index_key},
        #     timeout=1800,
        # )
        # response.raise_for_status()
        logging.info(f"Successfully ingested {index_key}")

    except requests.HTTPError as err:
        logging.error(err, exc_info=True)
        logging.error(f"HTTP error when ingesting {index_key}")
    except Exception as err:
        logging.error(err, exc_info=True)
        logging.error(f"Exception when ingesting {index_key}")
