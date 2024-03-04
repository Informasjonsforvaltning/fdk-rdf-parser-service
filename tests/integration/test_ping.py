"""Integration test cases for the ping route."""
import pytest
from fastapi.testclient import TestClient

from fdk_rdf_parser_service.app import app

client = TestClient(app)


@pytest.mark.integration
def test_ping() -> None:
    """Should return OK."""
    resp = client.get("/ping", timeout=15)
    assert resp.status_code == 200
