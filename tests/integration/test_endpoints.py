"""Integration test cases for the ping route."""
import json
from httpx import Response
import pytest
from fastapi.testclient import TestClient

from fdk_rdf_parser_service.app import app

from ..conftest import test_data_location

client = TestClient(app)


@pytest.mark.integration
def test_datasets_endpoint() -> None:
    """Should return status 200 and a JSON list with expected number of resources."""
    with open(f"{test_data_location}/dataset0.ttl", "r") as f:
        resp: Response = client.post(
            "/datasets",
            content=f.read(),
            headers={"Content-Type": "text/turtle"},
            timeout=15,
        )
        assert resp.status_code == 200

        data = json.loads(resp.json())
        assert len(data) == 1


@pytest.mark.integration
def test_data_services_endpoint() -> None:
    """Should return status 200 and a JSON list with expected number of resources."""
    with open(f"{test_data_location}/data_service0.ttl", "r") as f:
        resp: Response = client.post(
            "/data-services",
            content=f.read(),
            headers={"Content-Type": "text/turtle"},
            timeout=15,
        )
        assert resp.status_code == 200

        data = json.loads(resp.json())
        assert len(data) == 1


@pytest.mark.integration
def test_concepts_endpoint() -> None:
    """Should return status 200 and a JSON list with expected number of resources."""
    with open(f"{test_data_location}/concept0.ttl", "r") as f:
        resp: Response = client.post(
            "/concepts",
            content=f.read(),
            headers={"Content-Type": "text/turtle"},
            timeout=15,
        )
        assert resp.status_code == 200

        data = json.loads(resp.json())
        assert len(data) == 1


@pytest.mark.integration
def test_services_endpoint() -> None:
    """Should return status 200 and a JSON list with expected number of resources."""
    with open(f"{test_data_location}/service0.ttl", "r") as f:
        resp: Response = client.post(
            "/services",
            content=f.read(),
            headers={"Content-Type": "text/turtle"},
            timeout=15,
        )
        assert resp.status_code == 200

        data = json.loads(resp.json())
        assert len(data) == 1


@pytest.mark.integration
def test_events_endpoint() -> None:
    """Should return status 200 and a JSON list with expected number of resources."""
    with open(f"{test_data_location}/event0.ttl", "r") as f:
        resp: Response = client.post(
            "/events",
            content=f.read(),
            headers={"Content-Type": "text/turtle"},
            timeout=15,
        )
        assert resp.status_code == 200

        data = json.loads(resp.json())
        assert len(data) == 1


@pytest.mark.integration
def test_unspecified_catalog_type_returns_404() -> None:
    """Should return status 404."""
    with open(f"{test_data_location}/dataset0.ttl", "r") as f:
        resp: Response = client.post(
            "/",
            content=f.read(),
            headers={"Content-Type": "text/turtle"},
            timeout=15,
        )
        assert resp.status_code == 404


@pytest.mark.integration
def test_wrong_catalog_type_returns_404() -> None:
    """Should return status 404."""
    with open(f"{test_data_location}/dataset0.ttl", "r") as f:
        resp: Response = client.post(
            "/invalid-catalog-type",
            content=f.read(),
            headers={"Content-Type": "text/turtle"},
            timeout=15,
        )
        assert resp.status_code == 404
