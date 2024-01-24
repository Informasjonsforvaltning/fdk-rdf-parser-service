import dataclasses
import simplejson
import logging
from typing import Dict, List, Union
from rdflib.exceptions import ParserError, UniquenessError

from fdk_rdf_parser import (
    parse_concepts,
    parse_data_services,
    parse_datasets,
    parse_events,
    parse_information_models,
    parse_public_services,
)


from fdk_rdf_parser.classes import (
    Concept,
    Dataset,
    DataService,
    Event,
    InformationModel,
    PublicService,
)

import aiohttp
from fdk_rdf_parser_service.config import REASONING_HOST
from fdk_rdf_parser_service.model.parse_result import ParsedCatalog, RdfParseResult
from fdk_rdf_parser_service.model.rabbit_report import FdkIdAndUri, RabbitReport


async def handle_reports(reports: List[RabbitReport]):
    """Handle reports."""
    results: List[RdfParseResult] = [
        await handle_report(report) for report in reports if not report.harvestError
    ]

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
        except (ParserError, UniquenessError) as e:
            logging.warning(f"Failed to parse catalog {catalog.fdkId}: {e}")
            report.harvestError = True
    return RdfParseResult(parsedCatalogs=parsedCatalogs, report=report)


async def fetch_and_parse_catalog(
    catalog: FdkIdAndUri, catalogType: str
) -> ParsedCatalog:
    """Fetch and parse catalogs."""
    async with aiohttp.ClientSession() as session:
        rdf_data = await fetch_catalog(
            session, f"{REASONING_HOST}/{catalogType}/catalogs/{catalog.fdkId}"
        )
        return ParsedCatalog(
            catalogId=catalog.fdkId, jsonBody=parse_rdf_to_json(rdf_data, catalogType)
        )


async def fetch_catalog(session: aiohttp.ClientSession, url: str) -> str:
    """Fetch catalog from reports."""
    async with session.get(url) as response:
        status = response.status
        if status != 200:
            logging.warning(f"Failed to fetch catalog {url}, status {status}")
        return await response.text()


def parse_rdf_to_json(catalog_as_rdf: str, catalogType: str) -> str:
    """Parse RDF data to JSON."""
    return simplejson.dumps(
        [
            dataclasses.asdict(rdf_as_python_class)
            for rdf_as_python_class in parse_rdf_to_python_classes(
                catalog_as_rdf, catalogType
            )
        ],
        iterable_as_array=True,
    )


def parse_rdf_to_python_classes(catalog_as_rdf: str, catalogType: str):
    """Parse RDF data to Python classes."""
    parsed_data = parse_on_catalog_type(catalog_as_rdf, catalogType)
    return [rdf_as_python_class for rdf_as_python_class in parsed_data.values()]


def parse_on_catalog_type(
    rdf_data: str, catalogType: str
) -> Dict[
    str,
    Union[
        Concept,
        Dataset,
        DataService,
        Event,
        InformationModel,
        PublicService,
    ],
]:
    parsers = {
        "concepts": parse_concepts,
        "dataservices": parse_data_services,
        "datasets": parse_datasets,
        "events": parse_events,
        "informationmodels": parse_information_models,
        "public_services": parse_public_services,
    }
    parser = parsers.get(catalogType)
    if parser:
        return parser(rdf_data)
    else:
        return Dict()
