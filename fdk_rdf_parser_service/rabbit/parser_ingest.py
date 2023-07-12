"""Ingester for messages."""
import json
import logging

from fdk_rdf_parser_service.model.reasoning_report import ReasoningReport
from fdk_rdf_parser_service.service.parse_job import handle_reports


async def ingest_for_index(index_key: str, body: bytes) -> None:
    """Ingest messages."""
    try:
        reports = [ReasoningReport(**report) for report in json.loads(body)]
        logging.info(
            f"RabbitMQ ingesting index {index_key!r}, number of reports: {len(reports)} "
        )

        await handle_reports(reports)

    except Exception as err:
        logging.error(f"Exception when ingesting {index_key}: {err}")
