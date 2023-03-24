"""Integration test cases for the ready route."""
from typing import Any

from aiohttp.test_utils import TestClient as _TestClient
import pytest


@pytest.mark.integration
async def test_ready(docker_service: Any, aiohttp_client: _TestClient) -> None:
    """Should return OK."""
    resp = await aiohttp_client.get("/ready")
    assert resp.status == 200
