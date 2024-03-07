"""Function for doing parse job"""

from dataclasses import asdict
from typing import Callable, Dict
from fdk_rdf_parser import (
    parse_datasets,
    parse_concepts,
    parse_information_models,
    parse_public_services,
    parse_events,
    parse_data_services,
)

from fdk_rdf_parser_service.model import ResourceEnum, ResourceType


parser_func_map: Dict[ResourceEnum, Callable[[str], Dict[str, ResourceType]]] = {
    ResourceEnum.DATASET: parse_datasets,
    ResourceEnum.DATA_SERVICE: parse_data_services,
    ResourceEnum.CONCEPT: parse_concepts,
    ResourceEnum.INFORMATION_MODEL: parse_information_models,
    ResourceEnum.SERVICE: parse_public_services,
    ResourceEnum.EVENT: parse_events,
}


def parse_resource(
    rdf_data: str, resource_type: ResourceEnum
) -> Dict[str, Dict[str, ResourceType]]:
    """Parses RDF data according to the given resource type and returns it as a JSON string"""
    parser_func = parser_func_map[resource_type]

    parsed_data_json_serializable = {
        key: asdict(value) for key, value in parser_func(rdf_data).items()
    }

    return parsed_data_json_serializable
