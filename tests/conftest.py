"""Conftest module."""
from os import environ as env
import time
from typing import Any

from aiohttp.test_utils import TestClient as _TestClient
from dotenv import load_dotenv
import pytest
import requests
from requests.exceptions import ConnectionError

from fdk_rdf_parser_service import create_app

load_dotenv()
HOST_PORT = int(env.get("HOST_PORT", "8000"))


@pytest.mark.integration
@pytest.fixture
async def client(aiohttp_client: Any) -> _TestClient:
    """Instantiate server and start it."""
    app = await create_app()
    return await aiohttp_client(app)


def is_responsive(url: Any) -> Any:
    """Return true if response from service is 200."""
    url = f"{url}/ready"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            time.sleep(2)  # sleep extra 2 sec
            return True
    except ConnectionError:
        return False
