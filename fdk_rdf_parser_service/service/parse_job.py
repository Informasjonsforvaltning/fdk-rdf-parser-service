import logging
from typing import Callable, List

import aiohttp
from fdk_rdf_parser import (
    parse_concepts,
    parse_data_services,
    parse_datasets,
    parse_events,
    parse_information_models,
    parse_public_services,
)

from fdk_rdf_parser_service.model.reasoning_report import CatalogType, ReasoningReport


async def fetch_catalogs(report: ReasoningReport) -> List[str]:
    """Fetch catalogs."""
    get_responses = []
    if report.changedCatalogs:
        async with aiohttp.ClientSession() as session:
            for fdk_id_and_uri in report.changedCatalogs:
                if fdk_id_and_uri.uri:
                    get_responses.append(
                        await session.get(fdk_id_and_uri.uri, timeout=5)
                    )

    logging.info(f"Fetched {len(get_responses)} catalogs.")

    changed_catalogs_rdf = []
    for response in get_responses:
        if response.status == 200:
            changed_catalogs_rdf.append(await response.text())

    return changed_catalogs_rdf


async def handle_reports(reports: list[ReasoningReport]) -> None:
    """Handle reports."""
    for report in reports:
        catalogs = await fetch_catalogs(report)
        parse_function = get_parse_function(report.dataType)

        parsed_catalogs = [parse_function(catalog) for catalog in catalogs]
        logging.info(f"Number of parsed catalogs: {len(parsed_catalogs)}")

        post_catalogs(parsed_catalogs)


def get_parse_function(data_type: CatalogType | None) -> Callable:
    """Get parse function."""
    if data_type == CatalogType.CONCEPTS:
        return parse_concepts
    elif data_type == CatalogType.DATASERVICES:
        return parse_data_services
    elif data_type == CatalogType.DATASETS:
        return parse_datasets
    elif data_type == CatalogType.INFORMATIONMODELS:
        return parse_information_models
    elif data_type == CatalogType.EVENTS:
        return parse_events
    elif data_type == CatalogType.PUBLICSERVICES:
        return parse_public_services
    else:
        raise ValueError(f"Unknown dataType {data_type}")


def post_catalogs(parsed_catalogs: List[str]) -> None:
    logging.info(f"Posting {len(parsed_catalogs)} catalogs to db server.")
