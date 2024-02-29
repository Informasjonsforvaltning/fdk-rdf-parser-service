"""Contract test cases for the parse endpoints."""

from os import environ as env
from typing import Any
import pytest
import requests

HOST_PORT = env.get("HOST_PORT", "8080")
HOST_URL = f"http://localhost:{HOST_PORT}"


@pytest.mark.contract
async def test_dataset_endpoint(docker_services: Any) -> None:
    """Should return status 200 and a JSON list with 2 datasets."""
    with open("tests/test_data/datasets0.ttl", "r") as f:
        body = f.read()
        resp = await requests.post(f"{HOST_URL}/datasets", data=body, timeout=15)
        data = await resp.json()

        assert resp.status == 200
        assert len(data) == 1
