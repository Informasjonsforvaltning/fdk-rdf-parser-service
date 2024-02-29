"""Integration test cases for the parse routes."""
from aiohttp.test_utils import TestClient as _TestClient
import pytest


@pytest.mark.integration
async def test_dataset_endpoint(client: _TestClient) -> None:
    """Should return status 200 and a JSON list with 2 datasets."""
    with open("tests/test_data/datasets0.ttl", "r") as f:
        body = f.read()
        resp = await client.post("/datasets", data=body, timeout=15)
        data = await resp.json()

        assert resp.status == 200
        assert len(data) == 1
