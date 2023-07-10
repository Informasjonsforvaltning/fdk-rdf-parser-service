"""Ingester for messages."""
import json
import logging
from typing import Callable

# import requests

from fdk_rdf_parser import (
    parse_concepts,
    parse_data_services,
    parse_datasets,
    parse_events,
    parse_information_models,
    parse_public_services,
)

from fdk_rdf_parser_service.model.reasoning_report import CatalogType, ReasoningReport


def ingest_for_index(index_key: str, body: bytes) -> None:
    """Ingest messages."""
    try:
        reports = [ReasoningReport(**report) for report in json.loads(body)]
        logging.info(f"RabbitMQ ingesting index {index_key!r} ")
        logging.debug(f"Ingesting with reports {reports}")
        for report in reports:
            logging.info(f"Report URL: {report.url}, CatalogType {report.dataType}")
            logging.info(
                f"  Number of changed catalogs: {len(report.changedCatalogs) if report.changedCatalogs else 0}"
            )
            logging.info(
                f"  Number of changed resources: {len(report.changedResources) if report.changedResources else 0}"
            )
            fetch_catalogs(report)

    except Exception as err:
        logging.error(err, exc_info=True)
        logging.error(f"Exception when ingesting {index_key}: {err}")


def fetch_catalogs(report: ReasoningReport) -> None:
    """Parse report."""
    if report.changedCatalogs:
        for catalog_id_and_uri in report.changedCatalogs:
            logging.info(
                f"Catalog to fetch: id: {catalog_id_and_uri.fdkId}, uri: {catalog_id_and_uri.uri}"
            )

        # changedCatalogsRdf = [requests.get(url) for url in report.changedCatalogs]

        # for rdfGraph in changedCatalogsRdf:
        #     logging.debug(f"{rdfGraph}")
    logging.debug(f"Parser function returned: {get_parse_function(report.dataType)}")


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
