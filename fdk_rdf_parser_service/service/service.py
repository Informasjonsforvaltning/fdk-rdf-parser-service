"""Function for doing parse job"""

from dataclasses import asdict
import logging
from typing import Callable, Dict, Literal, Union
from fdk_rdf_parser import (
    parse_datasets,
    parse_concepts,
    parse_information_models,
    parse_public_services,
    parse_events,
    parse_data_services,
)
from fdk_rdf_parser.classes import (
    Dataset,
    Concept,
    InformationModel,
    PublicService,
    Event,
    DataService,
)
import simplejson

ResourceType = Union[
    Dataset,
    Concept,
    InformationModel,
    PublicService,
    Event,
    DataService,
]

CatalogType = Literal[
    "datasets",
    "data-services",
    "concepts",
    "information-models",
    "services",
    "events",
]

parser_func_map: Dict[CatalogType, Callable[[str], Dict[str, ResourceType]]] = {
    "datasets": parse_datasets,
    "data-services": parse_data_services,
    "concepts": parse_concepts,
    "information-models": parse_information_models,
    "services": parse_public_services,
    "events": parse_events,
}


def parse_resource(rdfData: str, catalogType: CatalogType) -> str:
    """Parses RDF data according to the given catalog type and returns it as a JSON string"""
    parser_func = parser_func_map[catalogType]
    try:
        parsedData = {key: asdict(value) for key, value in parser_func(rdfData).items()}
    except Exception as err:
        logging.warning(f"Failed to convert dataclasses to basic Python objects: {err}")
        raise
    try:
        jsonData = simplejson.dumps(parsedData, iterable_as_array=True)
    except Exception as err:
        logging.warning(f"Failed to convert parsed data to JSON: {err}")
        raise
    return jsonData
