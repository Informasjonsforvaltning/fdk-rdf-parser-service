"""Contract test cases for the parse endpoints."""

from typing import Any
import pytest
import requests

from ..conftest import test_data_location, HOST_PORT


@pytest.mark.contract
def test_datasets_endpoint(docker_ip: Any, docker_service: Any) -> None:
    """Should return status 200 and a JSON list with expected number of resources."""
    url = f"http://{docker_ip}:{HOST_PORT}"
    with open(f"{test_data_location}/dataset0.ttl", "r") as f:
        resp = requests.post(f"{url}/datasets", data=f.read(), timeout=60)
        assert resp.status_code == 200

        data = resp.json()
        assert len(data) == 1


@pytest.mark.contract
def test_dataservices_endpoint(docker_ip: Any, docker_service: Any) -> None:
    """Should return status 200 and a JSON list with expected number of resources."""
    url = f"http://{docker_ip}:{HOST_PORT}"
    with open(f"{test_data_location}/data_service0.ttl", "r") as f:
        resp = requests.post(f"{url}/data-services", data=f.read(), timeout=90)
        assert resp.status_code == 200

        data = resp.json()
        assert len(data) == 1


@pytest.mark.contract
def test_concepts_endpoint(docker_ip: Any, docker_service: Any) -> None:
    """Should return status 200 and a JSON list with expected number of resources."""
    url = f"http://{docker_ip}:{HOST_PORT}"
    with open(f"{test_data_location}/concept0.ttl", "r") as f:
        resp = requests.post(f"{url}/concepts", data=f.read(), timeout=90)
        assert resp.status_code == 200

        data = resp.json()
        assert len(data) == 1


@pytest.mark.contract
def test_information_models_endpoint(docker_ip: Any, docker_service: Any) -> None:
    """Should return status 200 and a JSON list with expected number of resources."""
    url = f"http://{docker_ip}:{HOST_PORT}"
    with open(f"{test_data_location}/information_model0.ttl", "r") as f:
        resp = requests.post(f"{url}/information-models", data=f.read(), timeout=90)
        assert resp.status_code == 200

        data = resp.json()
        assert len(data) == 1


@pytest.mark.contract
def test_services_endpoint(docker_ip: Any, docker_service: Any) -> None:
    """Should return status 200 and a JSON list with expected number of resources."""
    url = f"http://{docker_ip}:{HOST_PORT}"
    with open(f"{test_data_location}/service0.ttl", "r") as f:
        resp = requests.post(f"{url}/services", data=f.read(), timeout=90)
        assert resp.status_code == 200

        data = resp.json()
        assert len(data) == 1


@pytest.mark.contract
def test_events_endpoint(docker_ip: Any, docker_service: Any) -> None:
    """Should return status 200 and a JSON list with expected number of resources."""
    url = f"http://{docker_ip}:{HOST_PORT}"
    with open(f"{test_data_location}/event0.ttl", "r") as f:
        resp = requests.post(f"{url}/events", data=f.read(), timeout=60)
        assert resp.status_code == 200

        data = resp.json()
        assert len(data) == 1
