from enum import Enum


class CatalogType(Enum):
    CONCEPTS = "concept"
    DATASERVICES = "dataservice"
    DATASETS = "dataset"
    INFORMATIONMODELS = "informationmodel"
    EVENTS = "event"
    PUBLICSERVICES = "publicService"
