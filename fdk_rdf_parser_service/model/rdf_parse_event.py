from dataclasses import dataclass
import datetime
from typing import Literal

from dataclasses_json import DataClassJsonMixin

KafkaResourceType = Literal[
    "DATASET", "DATASERVICE", "CONCEPT", "INFORMATIONMODEL", "SERVICE", "EVENT"
]


@dataclass
class RdfParseEvent(DataClassJsonMixin):
    resourceType: KafkaResourceType
    fdkId: str
    data: str
    timestamp: datetime.datetime
