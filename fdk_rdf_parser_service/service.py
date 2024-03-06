"""Function for doing parse job"""

from dataclasses import asdict
import logging
from typing import Any, Callable, Dict
from fdk_rdf_parser import (
    parse_datasets,
    parse_concepts,
    parse_information_models,
    parse_public_services,
    parse_events,
    parse_data_services,
)

from fdk_rdf_parser_service.model import ResourceEnum


parser_func_map: Dict[ResourceEnum, Callable[[str], Dict[str, Any]]] = {
    ResourceEnum.DATASET: parse_datasets,
    ResourceEnum.DATA_SERVICE: parse_data_services,
    ResourceEnum.CONCEPT: parse_concepts,
    ResourceEnum.INFORMATION_MODEL: parse_information_models,
    ResourceEnum.SERVICE: parse_public_services,
    ResourceEnum.EVENT: parse_events,
}


def parse_resource(rdfData: str, resourceType: ResourceEnum) -> Dict[str, Any]:
    """Parses RDF data according to the given resource type and returns it as a JSON string"""
    parser_func = parser_func_map[resourceType]
    try:
        parsedData = {key: asdict(value) for key, value in parser_func(rdfData).items()}
    except Exception as err:
        logging.warning(f"Failed to convert dataclasses to basic Python objects: {err}")
        raise
    return parsedData
