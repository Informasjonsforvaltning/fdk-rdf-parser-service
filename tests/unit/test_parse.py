import pytest
from fdk_rdf_parser_service.model import CatalogEnum

from fdk_rdf_parser_service.service import parse_resource
from ..conftest import test_data_location


@pytest.mark.unit
def test_parse_datasets() -> None:
    """Should return the expected number of resources as JSON"""
    with open(f"{test_data_location}/dataset0.ttl", "r") as f:
        parsed_data = parse_resource(f.read(), CatalogEnum.DATASETS)
        assert len(parsed_data) == 1


@pytest.mark.unit
def test_parse_dataservices() -> None:
    """Should return the expected number of resources as JSON"""
    with open(f"{test_data_location}/data_service0.ttl", "r") as f:
        parsed_data = parse_resource(f.read(), CatalogEnum.DATA_SERVICES)
        assert len(parsed_data) == 1


@pytest.mark.unit
def test_parse_concepts() -> None:
    """Should return the expected number of resources as JSON"""
    with open(f"{test_data_location}/concept0.ttl", "r") as f:
        parsed_data = parse_resource(f.read(), CatalogEnum.CONCEPTS)
        assert len(parsed_data) == 1


@pytest.mark.unit
def test_parse_information_models() -> None:
    """Should return the expected number of resources as JSON"""
    with open(f"{test_data_location}/information_model0.ttl", "r") as f:
        parsed_data = parse_resource(f.read(), CatalogEnum.INFORMATION_MODELS)
        assert len(parsed_data) == 1


@pytest.mark.unit
def test_parse_services() -> None:
    """Should return the expected number of resources as JSON"""
    with open(f"{test_data_location}/service0.ttl", "r") as f:
        parsed_data = parse_resource(f.read(), CatalogEnum.SERVICES)
        assert len(parsed_data) == 1


@pytest.mark.unit
def test_parse_events() -> None:
    """Should return the expected number of resources as JSON"""
    with open(f"{test_data_location}/event0.ttl", "r") as f:
        parsed_data = parse_resource(f.read(), CatalogEnum.EVENTS)
        assert len(parsed_data) == 1
