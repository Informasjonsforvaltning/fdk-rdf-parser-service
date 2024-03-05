"""Integration test cases for the ping route."""
from typing import Any

import pytest
import requests


@pytest.mark.contract
def test_ping(docker_service: Any) -> None:
    """Should return OK."""
    result = requests.get(f"{docker_service}/ping")
    assert result.status_code == 200
