"""Ingester for messages."""
import json
import logging

from aiohttp import web
from aiohttp.web import HTTPException

from fdk_rdf_parser_service.model.reasoning_report import ReasoningReport
from fdk_rdf_parser_service.rabbit.producer import publish_parser_report
from fdk_rdf_parser_service.service.parse_job import handle_reports


async def ingest_for_index(app: web.Application, index_key: str, body: bytes) -> None:
    """Ingest messages."""
    try:
        reports = [ReasoningReport(**report) for report in json.loads(body)]
        logging.info(
            f"RabbitMQ ingesting index {index_key!r}, number of reports: {len(reports)} "
        )

        await handle_reports(reports)
        await publish_parser_report(app, success=True)
    except HTTPException as err:
        logging.warning(f"HTTPException when ingesting {index_key}: {err}")
        await publish_parser_report(app, success=False, msg=f"{err}")
    except Exception as err:
        logging.error(f"Unknown exception when ingesting {index_key}: {err}")
