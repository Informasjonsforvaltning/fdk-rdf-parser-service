"""Contract test cases for the parse endpoints."""

from typing import Any
import pytest
import requests

from ..conftest import test_data_location, TEST_API_KEY as api_key


@pytest.mark.contract
def test_datasets_endpoint(docker_service: Any) -> None:
    """Should return status 200 and a JSON list with expected number of resources."""
    with open(f"{test_data_location}/dataset0.ttl", "rb") as f:
        resp = requests.post(
            f"{docker_service}/dataset",
            data=f.read(),
            headers={"Content-Type": "text/turtle", "X-API-KEY": f"{api_key}"},
            timeout=10,
        )
        assert resp.status_code == 200
        assert resp.json()["type"] == "datasets"


@pytest.mark.contract
def test_dataservices_endpoint(docker_service: Any) -> None:
    """Should return status 200 and a JSON list with expected number of resources."""
    with open(f"{test_data_location}/data_service0.ttl", "rb") as f:
        resp = requests.post(
            f"{docker_service}/data-service",
            data=f.read(),
            headers={"Content-Type": "text/turtle", "X-API-KEY": f"{api_key}"},
            timeout=10,
        )
        assert resp.status_code == 200
        assert resp.json()["type"] == "dataservices"


@pytest.mark.contract
def test_concepts_endpoint(docker_service: Any) -> None:
    """Should return status 200 and a JSON list with expected number of resources."""
    with open(f"{test_data_location}/concept0.ttl", "rb") as f:
        resp = requests.post(
            f"{docker_service}/concept",
            data=f.read(),
            headers={"Content-Type": "text/turtle", "X-API-KEY": f"{api_key}"},
            timeout=10,
        )
        assert resp.status_code == 200
        assert resp.json()["type"] == "concept"


@pytest.mark.contract
def test_information_models_endpoint(docker_service: Any) -> None:
    """Should return status 200 and a JSON list with expected number of resources."""
    with open(f"{test_data_location}/information_model0.ttl", "rb") as f:
        resp = requests.post(
            f"{docker_service}/information-model",
            data=f.read(),
            headers={"Content-Type": "text/turtle", "X-API-KEY": f"{api_key}"},
            timeout=10,
        )
        assert resp.status_code == 200
        assert resp.json()["type"] == "informationmodels"


@pytest.mark.contract
def test_services_endpoint(docker_service: Any) -> None:
    """Should return status 200 and a JSON list with expected number of resources."""
    with open(f"{test_data_location}/service0.ttl", "rb") as f:
        resp = requests.post(
            f"{docker_service}/service",
            data=f.read(),
            headers={"Content-Type": "text/turtle", "X-API-KEY": f"{api_key}"},
            timeout=10,
        )
        assert resp.status_code == 200
        assert resp.json()["type"] == "publicservices"


@pytest.mark.contract
def test_events_endpoint(docker_service: Any) -> None:
    """Should return status 200 and a JSON list with expected number of resources."""
    with open(f"{test_data_location}/event0.ttl", "rb") as f:
        resp = requests.post(
            f"{docker_service}/event",
            data=f.read(),
            headers={"Content-Type": "text/turtle", "X-API-KEY": f"{api_key}"},
            timeout=10,
        )
        assert resp.status_code == 200
        data = resp.json()
        assert (
            data["specialized_type"] == "business_event"
            or data["specialized_type"] == "life_event"
        )


@pytest.mark.contract
def test_invalid_api_key(docker_service: Any) -> None:
    """Should return status 401."""
    with open(f"{test_data_location}/dataset0.ttl", "rb") as f:
        resp = requests.post(
            f"{docker_service}/dataset",
            data=f.read(),
            headers={"Content-Type": "text/turtle", "X-API-KEY": "invalid-key"},
            timeout=10,
        )
        assert resp.status_code == 401


@pytest.mark.contract
def test_multiple_resources_returns_400(docker_service: Any) -> None:
    """Should return status 400 Bad Request."""
    with open(f"{test_data_location}/multiple_datasets.ttl", "r") as f:
        resp = requests.post(
            f"{docker_service}/dataset",
            data=f.read(),
            headers={"Content-Type": "text/turtle", "X-API-KEY": f"{api_key}"},
            timeout=10,
        )
        assert resp.status_code == 400


@pytest.mark.contract
def test_bad_rdf_syntax_returns_400(docker_service: Any) -> None:
    """Should return status 400 Bad Request."""
    with open(f"{test_data_location}/bad_syntax.ttl", "r") as f:
        resp = requests.post(
            f"{docker_service}/dataset",
            data=f.read(),
            headers={"Content-Type": "text/turtle", "X-API-KEY": f"{api_key}"},
            timeout=10,
        )
        assert resp.status_code == 400
