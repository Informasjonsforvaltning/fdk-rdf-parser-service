"""Contract test cases for the parse endpoints."""

from typing import Any
import pytest
import requests
import simplejson

from ..conftest import test_data_location


@pytest.mark.contract
def test_datasets_endpoint(docker_service: Any) -> None:
    """Should return status 200 and a JSON list with expected number of resources."""
    with open(f"{test_data_location}/dataset0.ttl", "rb") as f:
        resp = requests.post(
            f"{docker_service}/dataset",
            data=f.read(),
            headers={"Content-Type": "text/turtle"},
            timeout=10,
        )
        assert resp.status_code == 200

        data = simplejson.loads(resp.json())
        assert len(data) == 1


@pytest.mark.contract
def test_dataservices_endpoint(docker_service: Any) -> None:
    """Should return status 200 and a JSON list with expected number of resources."""
    with open(f"{test_data_location}/data_service0.ttl", "rb") as f:
        resp = requests.post(
            f"{docker_service}/data-service",
            data=f.read(),
            headers={"Content-Type": "text/turtle"},
            timeout=10,
        )
        assert resp.status_code == 200

        data = simplejson.loads(resp.json())
        assert len(data) == 1


@pytest.mark.contract
def test_concepts_endpoint(docker_service: Any) -> None:
    """Should return status 200 and a JSON list with expected number of resources."""
    with open(f"{test_data_location}/concept0.ttl", "rb") as f:
        resp = requests.post(
            f"{docker_service}/concept",
            data=f.read(),
            headers={"Content-Type": "text/turtle"},
            timeout=10,
        )
        assert resp.status_code == 200

        data = simplejson.loads(resp.json())
        assert len(data) == 1


@pytest.mark.contract
def test_information_models_endpoint(docker_service: Any) -> None:
    """Should return status 200 and a JSON list with expected number of resources."""
    with open(f"{test_data_location}/information_model0.ttl", "rb") as f:
        resp = requests.post(
            f"{docker_service}/information-model",
            data=f.read(),
            headers={"Content-Type": "text/turtle"},
            timeout=10,
        )
        assert resp.status_code == 200

        data = simplejson.loads(resp.json())
        assert len(data) == 1


@pytest.mark.contract
def test_services_endpoint(docker_service: Any) -> None:
    """Should return status 200 and a JSON list with expected number of resources."""
    with open(f"{test_data_location}/service0.ttl", "rb") as f:
        resp = requests.post(
            f"{docker_service}/service",
            data=f.read(),
            headers={"Content-Type": "text/turtle"},
            timeout=10,
        )
        assert resp.status_code == 200

        data = simplejson.loads(resp.json())
        assert len(data) == 1


@pytest.mark.contract
def test_events_endpoint(docker_service: Any) -> None:
    """Should return status 200 and a JSON list with expected number of resources."""
    with open(f"{test_data_location}/event0.ttl", "rb") as f:
        resp = requests.post(
            f"{docker_service}/event",
            data=f.read(),
            headers={"Content-Type": "text/turtle"},
            timeout=10,
        )
        assert resp.status_code == 200

        data = simplejson.loads(resp.json())
        assert len(data) == 1
