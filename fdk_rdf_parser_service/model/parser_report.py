from dataclasses import dataclass
from typing import List, Optional

from fdk_rdf_parser_service.model.catalog_type import CatalogType


@dataclass
class FdkIdAndUri:
    fdkId: Optional[str] = None
    uri: Optional[str] = None


@dataclass
class ParserReport:
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
