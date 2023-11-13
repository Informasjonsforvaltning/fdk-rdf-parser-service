import pytest

from fdk_rdf_parser_service.model.rabbit_report import (
    FdkIdAndUri,
    RabbitReport,
)


@pytest.mark.unit
def test_json_parse_to_reasoning_report() -> None:
    """Should succeed on parsing json to ReasoningReport."""
    json_data = b"""
        {
            "id": "test-id",
            "url": "test-url",
            "dataType": "concept",
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
        dataType="concept",
        harvestError=False,
        startTime="test-startTime",
        endTime="test-endTime",
        errorMessage="test-errorMessage",
        changedCatalogs=[FdkIdAndUri(fdkId="test-fdkId", uri="test-uri")],
        changedResources=[],
        removedResources=[],
    )
    assert expected == RabbitReport.from_json(json_data)
