"""Integration test cases for the ready route."""
from typing import Any

import pytest
import requests


@pytest.mark.integration
async def test_fetch_rdf_graph(docker_service: Any) -> None:
    """Should return status code 200."""
    resp = requests.get(
        "http://localhost:8081/datasets/catalogs/a73bfe26-7cce-3989-822d-df5f7ee1080f",
        headers={"Accept": "text/turtle"},
        timeout=10,
    )
    assert resp.status_code == 200
