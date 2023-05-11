"""Dummy test."""

import pytest

from fdk_rdf_parser_service.model.reasoning_report import FdkIdAndUri, ReasoningReport


@pytest.mark.unit
def test_json_parse_to_reasoning_report() -> None:
    import json

    """Should succeed on parsing json to ReasoningReport."""
    json_data = b"""
        {
            "id": "test-id",
            "url": "test-url",
            "dataType": "test-dataType",
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
            "changedResources": null,
            "removedResources": null
        }
    """
    expected = ReasoningReport(
        id="test-id",
        url="test-url",
        dataType="test-dataType",
        harvestError=False,
        startTime="test-startTime",
        endTime="test-endTime",
        errorMessage="test-errorMessage",
        changedCatalogs=[FdkIdAndUri(fdkId="test-fdkId", uri="test-uri")],
        changedResources=None,
        removedResources=None,
    )
    assert expected == ReasoningReport(**json.loads(json_data))
