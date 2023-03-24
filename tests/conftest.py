"""Conftest module."""
import os
from os import environ as env
import time
from typing import Any

from aiohttp.test_utils import TestClient as _TestClient
from dotenv import load_dotenv
import pytest
import requests

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
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            time.sleep(2)  # sleep extra 2 sec
            return True
    except (ConnectionError, requests.ConnectionError):
        return False


@pytest.mark.integration
@pytest.mark.contract
@pytest.fixture(scope="session")
def http_service(docker_ip: Any, docker_services: Any) -> Any:
    """Ensure that HTTP service is up and responsive."""
    # `port_for` takes a container port and returns the corresponding host port
    port = docker_services.port_for("fdk-rdf-parser-service", HOST_PORT)
    url = "http://{}:{}".format(docker_ip, port)
    docker_services.wait_until_responsive(
        timeout=30.0, pause=0.5, check=lambda: is_responsive(url)
    )
    return url


@pytest.mark.integration
@pytest.mark.contract
@pytest.fixture(scope="session")
def docker_compose_file(pytestconfig: Any) -> Any:
    """Override default location of docker-compose.yaml file."""
    return os.path.join(str(pytestconfig.rootdir), "./", "docker-compose.yaml")


@pytest.mark.integration
@pytest.mark.contract
@pytest.fixture(scope="session")
def docker_cleanup(pytestconfig: Any) -> Any:
    """Override cleanup: do not remove containers in order to inspect logs."""
    return "stop"