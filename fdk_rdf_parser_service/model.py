from typing import Literal, Union, Dict

from fdk_rdf_parser.classes import (
    Dataset,
    Concept,
    InformationModel,
    PublicService,
    Event,
    DataService,
)

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

catalog_type_map: Dict[str, CatalogType] = {
    "datasets": "datasets",
    "data-services": "data-services",
    "concepts": "concepts",
    "information-models": "information-models",
    "services": "services",
    "events": "events",
}
