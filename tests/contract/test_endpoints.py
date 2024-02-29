"""Contract test cases for the parse endpoints."""

from typing import Any
import pytest
import requests

from ..conftest import test_data_location, HOST_PORT


@pytest.mark.contract
def test_dataset_endpoint(docker_ip: Any, docker_service: Any) -> None:
    """Should return status 200 and a JSON list with expected number of resources."""
    url = "http://{}:{}".format(docker_ip, HOST_PORT)
    with open(f"{test_data_location}/dataset0.ttl", "r") as f:
        resp = requests.post(f"{url}/datasets", data=f.read(), timeout=60)
        data = resp.json()

        assert resp.status_code == 200
        assert len(data) == 1


@pytest.mark.contract
def test_dataservice_endpoint(docker_ip: Any, docker_services: Any) -> None:
    """Should return status 200 and a JSON list with expected number of resources."""
    url = "http://{}:{}".format(docker_ip, HOST_PORT)
    with open(f"{test_data_location}/dataservice0.ttl", "r") as f:
        resp = requests.post(f"{url}/dataservices", data=f.read(), timeout=60)
        data = resp.json()

        assert resp.status_code == 200
        assert len(data) == 1
