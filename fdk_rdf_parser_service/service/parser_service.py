import dataclasses
import datetime
import simplejson
from typing import Any, Callable, Dict, List, Union


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

from fdk_rdf_parser_service.model.parse_result import (
    ParsedResource,
)
from fdk_rdf_parser_service.model.rdf_parse_event import (
    KafkaResourceType,
)


def handle_kafka_event(rdfData: str, catalogType: str) -> str:
    """Handle Kafka message."""
    parsed_resources = parse_rdf_to_classes(
        rdfData,
        catalogType,
    )

    return parsed_resources


def parse_rdf_to_classes(catalog_as_rdf: str, catalogType: str) -> List[ParsedResource]:
    """Parse RDF data to python classes."""
    parsed_resources: List[ParsedResource] = list()
    for fdkId, resource in parse_on_catalog_type(catalog_as_rdf, catalogType).items():
        parsed_resources.append(
            ParsedResource(
                fdkId=fdkId,
                resourceAsDict=dataclasses.asdict(resource),
                timestamp=datetime.datetime.now(datetime.timezone.utc),
            )
        )
    return parsed_resources


def convert_resources_to_json_list(resources: List[ParsedResource]) -> str:
    """Convert parsed resources to json."""
    return simplejson.dumps(
        [resource.resourceAsDict for resource in resources],
        iterable_as_array=True,
    )


def convert_resource_to_json(resourceAsDict: Dict[Any, Any]) -> str:
    return simplejson.dumps(resourceAsDict, iterable_as_array=True)


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
    parsers: Dict[KafkaResourceType, Callable] = {
        "CONCEPT": parse_concepts,
        "DATASERVICE": parse_data_services,
        "DATASET": parse_datasets,
        "EVENT": parse_events,
        "INFORMATIONMODEL": parse_information_models,
        "SERVICE": parse_public_services,
    }
    parser = parsers.get(catalogType)
    if parser:
        return parser(rdf_data)
    else:
        return dict()
