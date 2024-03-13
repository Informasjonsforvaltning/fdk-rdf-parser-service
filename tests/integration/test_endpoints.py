"""Integration test cases for the ping route."""

from httpx import Response
import pytest
from fastapi.testclient import TestClient

from fdk_rdf_parser_service.app import app

from ..conftest import test_data_location, TEST_API_KEY as api_key

client = TestClient(app)


@pytest.mark.integration
def test_dataset_endpoint() -> None:
    """Should return status 200 and a JSON list with expected number of resources."""
    with open(f"{test_data_location}/dataset0.ttl", "r") as f:
        resp: Response = client.post(
            "/dataset",
            content=f.read(),
            headers={"Content-Type": "text/turtle", "X-API-KEY": f"{api_key}"},
            timeout=15,
        )
        assert resp.status_code == 200

        data = resp.json()
        assert data["type"] == "datasets"


@pytest.mark.integration
def test_data_service_endpoint() -> None:
    """Should return status 200 and a JSON list with expected number of resources."""
    with open(f"{test_data_location}/data_service0.ttl", "r") as f:
        resp: Response = client.post(
            "/data-service",
            content=f.read(),
            headers={"Content-Type": "text/turtle", "X-API-KEY": f"{api_key}"},
            timeout=15,
        )
        assert resp.status_code == 200

        data = resp.json()
        assert data["type"] == "dataservices"


@pytest.mark.integration
def test_information_model_endpoint() -> None:
    """Should return status 200 and a JSON list with expected number of resources."""
    with open(f"{test_data_location}/information_model0.ttl", "r") as f:
        resp: Response = client.post(
            "/information-model",
            content=f.read(),
            headers={"Content-Type": "text/turtle", "X-API-KEY": f"{api_key}"},
            timeout=15,
        )
        assert resp.status_code == 200

        data = resp.json()
        assert data["type"] == "informationmodels"


@pytest.mark.integration
def test_concept_endpoint() -> None:
    """Should return status 200 and a JSON list with expected number of resources."""
    with open(f"{test_data_location}/concept0.ttl", "r") as f:
        resp: Response = client.post(
            "/concept",
            content=f.read(),
            headers={"Content-Type": "text/turtle", "X-API-KEY": f"{api_key}"},
            timeout=15,
        )
        assert resp.status_code == 200

        data = resp.json()
        assert data["type"] == "concept"


@pytest.mark.integration
def test_service_endpoint() -> None:
    """Should return status 200 and a JSON list with expected number of resources."""
    with open(f"{test_data_location}/service0.ttl", "r") as f:
        resp: Response = client.post(
            "/service",
            content=f.read(),
            headers={"Content-Type": "text/turtle", "X-API-KEY": f"{api_key}"},
            timeout=15,
        )
        assert resp.status_code == 200

        data = resp.json()
        assert data["type"] == "publicservices"


@pytest.mark.integration
def test_event_endpoint() -> None:
    """Should return status 200 and a JSON list with expected number of resources."""
    with open(f"{test_data_location}/event0.ttl", "r") as f:
        resp: Response = client.post(
            "/event",
            content=f.read(),
            headers={"Content-Type": "text/turtle", "X-API-KEY": f"{api_key}"},
            timeout=15,
        )
        assert resp.status_code == 200

        data = resp.json()
        assert (
            data["specialized_type"] == "business_event"
            or data["specialized_type"] == "life_event"
        )


@pytest.mark.integration
def test_unspecified_resource_type_returns_404() -> None:
    """Should return status 404."""
    with open(f"{test_data_location}/dataset0.ttl", "r") as f:
        resp: Response = client.post(
            "/",
            content=f.read(),
            headers={"Content-Type": "text/turtle", "X-API-KEY": f"{api_key}"},
            timeout=15,
        )
        assert resp.status_code == 404


@pytest.mark.integration
def test_wrong_resource_type_returns_404() -> None:
    """Should return status 404."""
    with open(f"{test_data_location}/dataset0.ttl", "r") as f:
        resp: Response = client.post(
            "/invalid-catalog-type",
            content=f.read(),
            headers={"Content-Type": "text/turtle", "X-API-KEY": f"{api_key}"},
            timeout=15,
        )
        assert resp.status_code == 404


@pytest.mark.integration
def test_multiple_resources_returns_400() -> None:
    """Should return status 400 Bad Request."""
    with open(f"{test_data_location}/multiple_datasets.ttl", "r") as f:
        resp: Response = client.post(
            "/dataset",
            content=f.read(),
            headers={"Content-Type": "text/turtle", "X-API-KEY": f"{api_key}"},
            timeout=15,
        )
        assert resp.status_code == 400


@pytest.mark.integration
def test_missing_resource_returns_400() -> None:
    """Should return status 400 Bad Request."""
    with open(f"{test_data_location}/missing_dataset.ttl", "r") as f:
        resp: Response = client.post(
            "/dataset",
            content=f.read(),
            headers={"Content-Type": "text/turtle", "X-API-KEY": f"{api_key}"},
            timeout=15,
        )
        assert resp.status_code == 400


@pytest.mark.integration
def test_bad_rdf_syntax_returns_400() -> None:
    """Should return status 400 Bad Request."""
    with open(f"{test_data_location}/bad_syntax.ttl", "r") as f:
        resp: Response = client.post(
            "/dataset",
            content=f.read(),
            headers={"Content-Type": "text/turtle", "X-API-KEY": f"{api_key}"},
            timeout=15,
        )
        assert resp.status_code == 400
