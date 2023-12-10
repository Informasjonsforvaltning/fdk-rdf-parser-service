from dataclasses import dataclass, field
from typing import List, Literal, Optional

from dataclasses_json import DataClassJsonMixin


@dataclass
class FdkIdAndUri(DataClassJsonMixin):
    fdkId: str
    uri: str


@dataclass
class RabbitReport(DataClassJsonMixin):
    id: str
    url: str
    dataType: Literal[
        "concept",
        "dataservice",
        "dataset",
        "informationmodel",
        "event",
        "publicService",
    ]
    harvestError: bool
    startTime: str
    endTime: str
    errorMessage: Optional[str] = None
    changedCatalogs: List[FdkIdAndUri] = field(default_factory=list)
    changedResources: List[FdkIdAndUri] = field(default_factory=list)
    removedResources: List[FdkIdAndUri] = field(default_factory=list)