import pytest
import simplejson

from fdk_rdf_parser_service.service.service import parse_resource


@pytest.mark.unit
def test_parse_dataset() -> None:
    """Should return the expected number of resources as JSON"""
    with open("tests/test_data/datasets0.ttl", "r") as f:
        rdfData = f.read()
        jsonData = parse_resource(rdfData, "datasets")

        assert len(simplejson.loads(jsonData)) == 1
