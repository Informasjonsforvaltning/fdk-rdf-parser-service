"""Integration test cases for the ping route."""
from typing import Any
from aiohttp.test_utils import TestClient as _TestClient
import pytest


@pytest.mark.integration
async def test_ready(http_service: Any, client: _TestClient) -> None:
    """Should return OK."""
    resp = await client.get("/ping")
    assert resp.status == 200
