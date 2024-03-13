import pytest

from fdk_rdf_parser_service.model import ResourceEnum

from fdk_rdf_parser_service.service import parse_resource
from ..conftest import test_data_location


@pytest.mark.unit
def test_parse_datasets() -> None:
    """Should return the expected number of resources as JSON"""
    with open(f"{test_data_location}/dataset0.ttl", "r") as f:
        resource_as_dict = parse_resource(f.read(), ResourceEnum.DATASET)
        assert resource_as_dict["type"] == "datasets"


@pytest.mark.unit
def test_parse_dataservices() -> None:
    """Should return the expected number of resources as JSON"""
    with open(f"{test_data_location}/data_service0.ttl", "r") as f:
        resource_as_dict = parse_resource(f.read(), ResourceEnum.DATA_SERVICE)
        assert resource_as_dict["type"] == "dataservices"


@pytest.mark.unit
def test_parse_concepts() -> None:
    """Should return the expected number of resources as JSON"""
    with open(f"{test_data_location}/concept0.ttl", "r") as f:
        resource_as_dict = parse_resource(f.read(), ResourceEnum.CONCEPT)
        assert resource_as_dict["type"] == "concept"


@pytest.mark.unit
def test_parse_information_models() -> None:
    """Should return the expected number of resources as JSON"""
    with open(f"{test_data_location}/information_model0.ttl", "r") as f:
        resource_as_dict = parse_resource(f.read(), ResourceEnum.INFORMATION_MODEL)
        assert resource_as_dict["type"] == "informationmodels"


@pytest.mark.unit
def test_parse_services() -> None:
    """Should return the expected number of resources as JSON"""
    with open(f"{test_data_location}/service0.ttl", "r") as f:
        resource_as_dict = parse_resource(f.read(), ResourceEnum.SERVICE)
        assert resource_as_dict["type"] == "publicservices"


@pytest.mark.unit
def test_parse_events() -> None:
    """Should return the expected number of resources as JSON"""
    with open(f"{test_data_location}/event0.ttl", "r") as f:
        resource_as_dict = parse_resource(f.read(), ResourceEnum.EVENT)
        assert (
            resource_as_dict["specialized_type"] == "business_event"
            or resource_as_dict["specialized_type"] == "life_event"
        )
