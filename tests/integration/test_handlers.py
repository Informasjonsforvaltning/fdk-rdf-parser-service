"""Integration test cases for the parse routes."""
from aiohttp.test_utils import TestClient as _TestClient
import pytest

from ..conftest import test_data_location


@pytest.mark.integration
async def test_datasets_endpoint(client: _TestClient) -> None:
    """Should return status 200 and a JSON list with expected number of resources."""
    with open(f"{test_data_location}/dataset0.ttl", "r") as f:
        resp = await client.post("/datasets", data=f.read(), timeout=30)
        assert resp.status == 200

        data = await resp.json()
        assert len(data) == 1


@pytest.mark.integration
async def test_dataservices_endpoint(client: _TestClient) -> None:
    """Should return status 200 and a JSON list with expected number of resources."""
    with open(f"{test_data_location}/data_service0.ttl", "r") as f:
        resp = await client.post("/data-services", data=f.read(), timeout=30)
        assert resp.status == 200

        data = await resp.json()
        assert len(data) == 1


@pytest.mark.integration
async def test_concepts_endpoint(client: _TestClient) -> None:
    """Should return status 200 and a JSON list with expected number of resources."""
    with open(f"{test_data_location}/concept0.ttl", "r") as f:
        resp = await client.post("/concepts", data=f.read(), timeout=30)
        assert resp.status == 200

        data = await resp.json()
        assert len(data) == 1


@pytest.mark.integration
async def test_information_models_endpoint(client: _TestClient) -> None:
    """Should return status 200 and a JSON list with expected number of resources."""
    with open(f"{test_data_location}/information_model0.ttl", "r") as f:
        resp = await client.post("/information-models", data=f.read(), timeout=30)
        assert resp.status == 200

        data = await resp.json()
        assert len(data) == 1


@pytest.mark.integration
async def test_events_endpoint(client: _TestClient) -> None:
    """Should return status 200 and a JSON list with expected number of resources."""
    with open(f"{test_data_location}/event0.ttl", "r") as f:
        resp = await client.post("/events", data=f.read(), timeout=30)
        assert resp.status == 200

        data = await resp.json()
        assert len(data) == 1
