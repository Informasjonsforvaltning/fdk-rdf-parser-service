"""Integration test cases for the ready route."""
from typing import Any
from aiohttp.test_utils import TestClient as _TestClient
import pytest


@pytest.mark.integration
async def test_ready(http_service: Any, client: _TestClient) -> None:
    """Should return OK."""
    resp = await client.get("/ready")
    assert resp.status == 200
