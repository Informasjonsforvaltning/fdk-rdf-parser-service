from dataclasses import dataclass
from typing import List

from dataclasses_json import DataClassJsonMixin

from fdk_rdf_parser_service.model.rabbit_report import RabbitReport


@dataclass
class ParsedCatalog(DataClassJsonMixin):
    catalogId: str
    jsonBody: str


@dataclass
class RdfParseResult(DataClassJsonMixin):
    parsedCatalogs: List[ParsedCatalog]
    report: RabbitReport
