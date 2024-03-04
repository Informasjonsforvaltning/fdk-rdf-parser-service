"""Conftest module."""
import os
from os import environ as env
from typing import Any

from dotenv import load_dotenv
import pytest
import requests

load_dotenv()
HOST_PORT = int(env.get("HOST_PORT", "8080"))

test_data_location = "tests/data"


def is_responsive(url: Any) -> Any:
    """Return true if response from service is 200."""
    url = f"{url}/ready"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return True
    except (ConnectionError, requests.ConnectionError):
        return False


@pytest.mark.contract
@pytest.fixture(scope="session")
def docker_service(docker_ip: Any, docker_services: Any) -> Any:
    """Ensure that HTTP service is up and responsive."""
    # `port_for` takes a container port and returns the corresponding host port
    port = docker_services.port_for("fdk-rdf-parser-service", HOST_PORT)
    url = "http://{}:{}".format(docker_ip, port)
    docker_services.wait_until_responsive(
        timeout=90.0, pause=1.0, check=lambda: is_responsive(url)
    )
    return url


@pytest.mark.contract
@pytest.fixture(scope="session")
def docker_compose_file(pytestconfig: Any) -> Any:
    """Override default location of docker-compose.yaml file."""
    return os.path.join(str(pytestconfig.rootdir), "./", "docker-compose.yaml")


@pytest.mark.contract
@pytest.fixture(scope="session")
def docker_cleanup(pytestconfig: Any) -> Any:
    """Override cleanup: do not remove containers in order to inspect logs."""
    return "stop"
