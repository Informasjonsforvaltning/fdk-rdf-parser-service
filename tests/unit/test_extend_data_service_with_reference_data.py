import pytest

from fdk_rdf_parser_service.parser.classes import (
    DataService,
    MediaTypeOrExtent,
    MediaTypeOrExtentType,
    ReferenceDataCode,
)
from fdk_rdf_parser_service.parser.reference_data import (
    DataServiceReferenceData,
    extend_data_service_with_reference_data,
)

from ..testdata import data_service_reference_data


@pytest.mark.unit
def test_handles_missing_references() -> None:
    parsed_data_service = DataService(
        mediaType=[ReferenceDataCode(uri="http://example.com/media-type/text/csv")],
        fdkFormat=[MediaTypeOrExtent(code="http://example.com/media-type/text/csv")],
    )

    assert (
        extend_data_service_with_reference_data(
            parsed_data_service, DataServiceReferenceData()
        )
        == DataService()
    )


@pytest.mark.unit
def test_handles_empty_media_type() -> None:
    parsed_data_service = DataService(
        mediaType=[ReferenceDataCode()],
        fdkFormat=[MediaTypeOrExtent()],
    )

    assert (
        extend_data_service_with_reference_data(
            parsed_data_service, data_service_reference_data
        )
        == parsed_data_service
    )


@pytest.mark.unit
def test_extend_media_types() -> None:
    parsed_data_service = DataService(
        mediaType=[
            ReferenceDataCode(
                uri="https://www.iana.org/assignments/media-types/text/csv"
            ),
            ReferenceDataCode(
                uri="http://publications.europa.eu/resource/authority/file-type/XML"
            ),
            ReferenceDataCode(uri="http://example.com/media-type/not/found"),
        ],
        fdkFormat=[
            MediaTypeOrExtent(
                uri="https://www.iana.org/assignments/media-types/text/csv"
            ),
            MediaTypeOrExtent(
                uri="http://publications.europa.eu/resource/authority/file-type/XML"
            ),
            MediaTypeOrExtent(uri="http://example.com/media-type/not/found"),
            MediaTypeOrExtent(code="some-type"),
        ],
    )

    expected = DataService(
        mediaType=[
            ReferenceDataCode(
                uri="https://www.iana.org/assignments/media-types/text/csv",
                code="text/csv",
                prefLabel={"nb": "text/csv"},
            ),
            ReferenceDataCode(
                uri="http://publications.europa.eu/resource/authority/file-type/XML",
                code="XML",
                prefLabel={"nb": "XML"},
            ),
        ],
        fdkFormat=[
            MediaTypeOrExtent(
                uri="https://www.iana.org/assignments/media-types/text/csv",
                type=MediaTypeOrExtentType.MEDIA_TYPE,
                name="csv",
                code="text/csv",
            ),
            MediaTypeOrExtent(
                uri="http://publications.europa.eu/resource/authority/file-type/XML",
                type=MediaTypeOrExtentType.FILE_TYPE,
                name="XML",
                code="XML",
            ),
            MediaTypeOrExtent(
                code="some-type",
                type=MediaTypeOrExtentType.UNKNOWN,
            ),
        ],
    )

    assert (
        extend_data_service_with_reference_data(
            parsed_data_service, data_service_reference_data
        )
        == expected
    )