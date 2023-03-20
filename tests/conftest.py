"""Conftest module."""
from os import environ as env
from typing import Any

from aiohttp.test_utils import TestClient as _TestClient
from dotenv import load_dotenv
import pytest

from fdk_rdf_parser_service import create_app

load_dotenv()
HOST_PORT = int(env.get("HOST_PORT", "8000"))


@pytest.mark.integration
@pytest.fixture
async def client(aiohttp_client: Any) -> _TestClient:
    """Instantiate server and start it."""
    app = await create_app()
    return await aiohttp_client(app)
