from enum import Enum
from typing import List, Optional

from pydantic.dataclasses import dataclass


class CatalogType(Enum):
    CONCEPTS = "concept"
    DATASERVICES = "dataservice"
    DATASETS = "dataset"
    INFORMATIONMODELS = "informationmodel"
    EVENTS = "event"
    PUBLICSERVICES = "publicService"


@dataclass
class FdkIdAndUri:
    fdkId: Optional[str] = None
    uri: Optional[str] = None


@dataclass
class ReasoningReport:
    id: Optional[str] = None
    url: Optional[str] = None
    dataType: Optional[CatalogType] = None
    harvestError: Optional[bool] = None
    startTime: Optional[str] = None
    endTime: Optional[str] = None
    errorMessage: Optional[str] = None
    changedCatalogs: Optional[List["FdkIdAndUri"]] = None
    changedResources: Optional[List["FdkIdAndUri"]] = None
    removedResources: Optional[List["FdkIdAndUri"]] = None
