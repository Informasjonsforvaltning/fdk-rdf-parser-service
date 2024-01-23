import logging
from typing import List

import aiohttp
from fdk_rdf_parser_service.config import REASONING_HOST
from fdk_rdf_parser_service.model.parse_result import ParsedCatalog, RdfParseResult
from fdk_rdf_parser_service.model.rabbit_report import FdkIdAndUri, RabbitReport


async def handle_reports(reports: List[RabbitReport]):
    """Handle reports."""
    results: List[RdfParseResult] = [
        await handle_report(report) for report in reports if not report.harvestError
    ]

    # Sorter i vellykkede og mislykkede parsinger
    successful = [result for result in results if not result.report.harvestError]
    failed = [result for result in results if result.report.harvestError]
    logging.info(
        f"All reports handled. Successful: {len(successful)}, failed: {len(failed)}"
    )
    if failed:
        logging.info("Some reports failed.")
        for result in failed:
            logging.info(
                f"Failed report id: {result.report.id}, report url: {result.report.url}"
            )
    return None


async def handle_report(report: RabbitReport) -> RdfParseResult:
    """Handle catalogs in report."""
    parsedCatalogs = []
    for catalog in report.changedCatalogs:
        try:
            parsedCatalog = await fetch_and_parse_catalog(catalog, report.dataType)
            parsedCatalogs.append(parsedCatalog)
        except Exception as e:
            logging.warning(f"Failed to parse catalog {catalog.fdkId}")
            logging.debug(e)
            report.harvestError = True
    return RdfParseResult(parsedCatalogs=parsedCatalogs, report=report)


async def fetch_and_parse_catalog(
    catalog: FdkIdAndUri, catalogType: str
) -> ParsedCatalog:
    """Fetch and parse catalogs."""
    async with aiohttp.ClientSession() as session:
        rdfData = await fetch_catalog(
            session, f"{REASONING_HOST}/{catalogType}/catalogs/{catalog.fdkId}"
        )
        return ParsedCatalog(
            catalogId=catalog.fdkId, jsonBody=parse_rdf(rdfData, catalogType)
        )


async def fetch_catalog(session: aiohttp.ClientSession, url: str) -> str:
    """Fetch catalog from reports."""
    async with session.get(url) as response:
        status = response.status
        if status != 200:
            logging.warning(f"Failed to fetch catalog {url}, status {status}")
        return await response.text()


def parse_rdf(rdfData: str, catalogType: str) -> str:
    """Parse RDF data to JSON."""
    # TODO: Implement RDF parsing
    logging.debug(f"parsing data: {rdfData[0:30]}, type: {catalogType}")
    return ""
