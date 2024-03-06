from enum import Enum
from typing import Union, Dict

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


class CatalogEnum(Enum):
    DATASETS = "datasets"
    DATA_SERVICES = "data-services"
    CONCEPTS = "concepts"
    INFORMATION_MODELS = "information-models"
    SERVICES = "services"
    EVENTS = "events"


catalog_type_map: Dict[str, CatalogEnum] = {
    "datasets": CatalogEnum.DATASETS,
    "data-services": CatalogEnum.DATA_SERVICES,
    "concepts": CatalogEnum.CONCEPTS,
    "information-models": CatalogEnum.INFORMATION_MODELS,
    "services": CatalogEnum.SERVICES,
    "events": CatalogEnum.EVENTS,
}
