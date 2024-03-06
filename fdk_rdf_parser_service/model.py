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
    DATASETS = "dataset"
    DATA_SERVICES = "data-service"
    CONCEPTS = "concept"
    INFORMATION_MODELS = "information-model"
    SERVICES = "service"
    EVENTS = "event"


catalog_type_map: Dict[str, CatalogEnum] = {
    "dataset": CatalogEnum.DATASETS,
    "data-service": CatalogEnum.DATA_SERVICES,
    "concept": CatalogEnum.CONCEPTS,
    "information-model": CatalogEnum.INFORMATION_MODELS,
    "service": CatalogEnum.SERVICES,
    "event": CatalogEnum.EVENTS,
}
