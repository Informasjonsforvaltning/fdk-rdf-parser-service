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


class ResourceEnum(Enum):
    DATASET = "dataset"
    DATA_SERVICE = "data-service"
    CONCEPT = "concept"
    INFORMATION_MODEL = "information-model"
    SERVICE = "service"
    EVENT = "event"


resource_type_map: Dict[str, ResourceEnum] = {
    "dataset": ResourceEnum.DATASET,
    "data-service": ResourceEnum.DATA_SERVICE,
    "concept": ResourceEnum.CONCEPT,
    "information-model": ResourceEnum.INFORMATION_MODEL,
    "service": ResourceEnum.SERVICE,
    "event": ResourceEnum.EVENT,
}
