from dataclasses import dataclass
import datetime
from typing import Any, Dict, List

from dataclasses_json import DataClassJsonMixin


@dataclass
class ParsedResource(DataClassJsonMixin):
    fdkId: str
    resourceAsDict: Dict[Any, Any]
    timestamp: datetime.datetime


@dataclass
class ParsedCatalog(DataClassJsonMixin):
    catalogId: str
    resources: List[ParsedResource]


@dataclass
class RdfParseResult(DataClassJsonMixin):
    parsedCatalogs: List[ParsedCatalog]
