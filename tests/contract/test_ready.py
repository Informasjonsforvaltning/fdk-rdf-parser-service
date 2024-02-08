"""Integration test cases for the ping route."""
from typing import Any

import pytest
import requests

fdk_rdf_parser_service_url = "http://localhost:8080"


@pytest.mark.contract
def test_ready(docker_service: Any) -> None:
    """Should return OK."""
    result = requests.get(f"{fdk_rdf_parser_service_url}/ping")
    assert result.status_code == 200
