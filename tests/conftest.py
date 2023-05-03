"""Conftest module."""
import json
import os
from os import environ as env
import time
from typing import Any
from unittest.mock import Mock

from aiohttp.test_utils import TestClient as _TestClient
from dotenv import load_dotenv
import pytest
from pytest_mock import MockFixture
import requests

from fdk_rdf_parser_service.app import create_app

load_dotenv()
HOST_PORT = int(env.get("HOST_PORT", "8080"))


@pytest.mark.integration
@pytest.fixture
async def aiohttp_client(aiohttp_client: Any) -> _TestClient:
    """Instantiate server and start it."""
    app = await create_app()
    return await aiohttp_client(app)


def is_responsive(url: Any) -> Any:
    """Return true if response from service is 200."""
    url = f"{url}/ready"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            time.sleep(2)  # sleep extra 2 sec
            return True
    except (ConnectionError, requests.ConnectionError):
        return False


@pytest.mark.integration
@pytest.mark.contract
@pytest.fixture(scope="session")
def docker_service(docker_ip: Any, docker_services: Any) -> Any:
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


def reference_effect(*args: Any, **kwargs: Any) -> Mock:
    rsp = Mock(spec=requests.Response)
    rsp.status_code = 200
    rsp.raise_for_status.return_value = None

    return add_reference_response_to_mock(rsp, args[0])


def add_reference_response_to_mock(mock: Mock, url: str) -> Mock:
    if "provenance-statements" in url:
        mock.json.return_value = json.load(
            open("./tests/json_data/provenancestatement.json")
        )
    elif "eu/access-rights" in url:
        mock.json.return_value = json.load(
            open("./tests/json_data/rightsstatement.json")
        )
    elif "eu/frequencies" in url:
        mock.json.return_value = json.load(open("./tests/json_data/frequency.json"))
    elif "linguistic-systems" in url:
        mock.json.return_value = json.load(
            open("./tests/json_data/linguisticsystem.json")
        )
    elif "reference-types" in url:
        mock.json.return_value = json.load(
            open("./tests/json_data/referencetypes.json")
        )
    elif "open-licenses" in url:
        mock.json.return_value = json.load(open("./tests/json_data/openlicenses.json"))
    elif "nasjoner" in url:
        mock.json.return_value = json.load(open("./tests/json_data/nasjoner.json"))
    elif "fylker" in url:
        mock.json.return_value = json.load(open("./tests/json_data/fylker.json"))
    elif "kommuner" in url:
        mock.json.return_value = json.load(open("./tests/json_data/kommuner.json"))
    elif "iana/media-types" in url:
        mock.json.return_value = json.load(open("./tests/json_data/mediatypes.json"))
    elif "eu/file-types" in url:
        mock.json.return_value = json.load(open("./tests/json_data/filetypes.json"))
    elif "schema/week-days" in url:
        mock.json.return_value = json.load(open("./tests/json_data/weekdays.json"))
    elif "adms/statuses" in url:
        mock.json.return_value = json.load(open("./tests/json_data/statuses.json"))
    elif "eu/main-activities" in url:
        mock.json.return_value = json.load(open("./tests/json_data/types.json"))
    elif "digdir/evidence-types" in url:
        mock.json.return_value = json.load(open("./tests/json_data/evidencetypes.json"))
    elif "/digdir/service-channel-types" in url:
        mock.json.return_value = json.load(
            open("./tests/json_data/serviceChannelTypes.json")
        )
    elif "adms/publisher-types" in url:
        mock.json.return_value = json.load(
            open("./tests/json_data/publishertypes.json")
        )
    elif "digdir/role-types" in url:
        mock.json.return_value = json.load(open("./tests/json_data/roletypes.json"))

    return mock


@pytest.fixture
def mock_reference_data_client(mocker: MockFixture) -> Mock:
    mock = mocker.patch("requests.get")
    mock.side_effect = reference_effect
    return mock


@pytest.fixture
def mock_reference_data_client_http_error(mocker: MockFixture) -> Mock:
    mock = mocker.patch("requests.get")
    mock.side_effect = requests.HTTPError(
        "reference-data-not-found",
        404,
        "Not Found",
        {},
        None,
    )
    return mock


@pytest.fixture
def mock_reference_data_client_timeout_error(mocker: MockFixture) -> Mock:
    mock = mocker.patch("requests.get")
    mock.side_effect = TimeoutError("connection to reference-data timed out")
    return mock


@pytest.fixture
def mock_reference_data_client_parse_error(mocker: MockFixture) -> Mock:
    mock = mocker.patch("requests.get")
    mock.side_effect = json.JSONDecodeError(msg="reference-parse-error", doc="", pos=0)
    return mock
