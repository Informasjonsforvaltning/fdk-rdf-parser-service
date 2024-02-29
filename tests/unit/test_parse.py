import pytest
import simplejson

from fdk_rdf_parser_service.service.service import parse_resource
from ..conftest import test_data_location


@pytest.mark.unit
def test_parse_datasets() -> None:
    """Should return the expected number of resources as JSON"""
    with open(f"{test_data_location}/dataset0.ttl", "r") as f:
        jsonData = parse_resource(f.read(), "datasets")
        assert len(simplejson.loads(jsonData)) == 1


@pytest.mark.unit
def test_parse_dataservices() -> None:
    """Should return the expected number of resources as JSON"""
    with open(f"{test_data_location}/dataservice0.ttl", "r") as f:
        jsonData = parse_resource(f.read(), "dataservices")
        assert len(simplejson.loads(jsonData)) == 1


@pytest.mark.unit
def test_parse_concepts() -> None:
    """Should return the expected number of resources as JSON"""
    with open(f"{test_data_location}/concept0.ttl", "r") as f:
        jsonData = parse_resource(f.read(), "concepts")
        assert len(simplejson.loads(jsonData)) == 1
