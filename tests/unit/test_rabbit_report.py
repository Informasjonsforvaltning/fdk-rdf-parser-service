import pytest

from fdk_rdf_parser_service.model.rabbit_report import (
    FdkIdAndUri,
    RabbitReport,
)
from fdk_rdf_parser_service.rabbit.consumer import parse_json_body_reports_list


@pytest.mark.unit
def test_json_decode_to_reasoning_report() -> None:
    """Should succeed on parsing json to ReasoningReport."""
    json_data = b"""
        {
            "id": "test-id",
            "url": "test-url",
            "dataType": "concepts",
            "harvestError": false,
            "startTime": "test-startTime",
            "endTime": "test-endTime",
            "errorMessage": "test-errorMessage",
            "changedCatalogs": [
                {
                    "fdkId": "test-fdkId",
                    "uri": "test-uri"
                }
            ],
            "changedResources": [],
            "removedResources": []
        }
    """
    expected = RabbitReport(
        id="test-id",
        url="test-url",
        dataType="concepts",
        harvestError=False,
        startTime="test-startTime",
        endTime="test-endTime",
        errorMessage="test-errorMessage",
        changedCatalogs=[FdkIdAndUri(fdkId="test-fdkId", uri="test-uri")],
        changedResources=[],
        removedResources=[],
    )
    assert expected == RabbitReport.from_json(json_data)


@pytest.mark.unit
def test_json_decode_list_of_reports() -> None:
    """Should succeed on parsing json list of reports to ReasoningReport."""
    json_data = b"""
        [
            {
                "id": "4da7d1f5-4da0-426c-a9ee-10e8692675fb",
                "url": "https://dataut.vegvesen.no/catalog.ttl",
                "dataType": "datasets",
                "harvestError": false,
                "startTime": "2024-01-18 12:38:13 +0100",
                "endTime": "2024-01-18 12:38:15 +0100",
                "errorMessage": null,
                "changedCatalogs": [
                    {
                        "fdkId": "3f500813-1f1f-3175-86e3-8f8e252ff176",
                        "uri": "https://ramuzzi.com/informasjonsmodeller#Katalog"
                    }
                ],
                "changedResources": [],
                "removedResources": []
            },
            {
                "id": "test-id",
                "url": "test-url",
                "dataType": "concepts",
                "harvestError": false,
                "startTime": "test-startTime",
                "endTime": "test-endTime",
                "errorMessage": "test-errorMessage",
                "changedCatalogs": [
                    {
                        "fdkId": "test-fdkId",
                        "uri": "test-uri"
                    }
                ],
                "changedResources": [],
                "removedResources": []
            }
        ]
    """
    expected = [
        RabbitReport(
            id="4da7d1f5-4da0-426c-a9ee-10e8692675fb",
            url="https://dataut.vegvesen.no/catalog.ttl",
            dataType="datasets",
            harvestError=False,
            startTime="2024-01-18 12:38:13 +0100",
            endTime="2024-01-18 12:38:15 +0100",
            errorMessage=None,
            changedCatalogs=[
                FdkIdAndUri(
                    fdkId="3f500813-1f1f-3175-86e3-8f8e252ff176",
                    uri="https://ramuzzi.com/informasjonsmodeller#Katalog",
                )
            ],
            changedResources=[],
            removedResources=[],
        ),
        RabbitReport(
            id="test-id",
            url="test-url",
            dataType="concepts",
            harvestError=False,
            startTime="test-startTime",
            endTime="test-endTime",
            errorMessage="test-errorMessage",
            changedCatalogs=[FdkIdAndUri(fdkId="test-fdkId", uri="test-uri")],
            changedResources=[],
            removedResources=[],
        ),
    ]
    assert expected == parse_json_body_reports_list(json_data)
