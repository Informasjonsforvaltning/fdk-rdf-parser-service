import json
import pytest

from fdk_rdf_parser_service.service.parser_service import (
    convert_resources_to_json,
    parse_rdf_to_classes,
)


@pytest.mark.unit
def test_parse_dataset() -> None:
    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix xsd:   <http://www.w3.org/2001/XMLSchema#> .
        @prefix dcat:  <http://www.w3.org/ns/dcat#> .
        @prefix foaf:  <http://xmlns.com/foaf/0.1/> .

        <https://testdirektoratet.no/model/dataset/0>
                a                         dcat:Dataset ;
                dct:accrualPeriodicity
                    <http://publications.europa.eu/resource/authority/freq> ;
                dct:identifier
                    "adb4cf00-31c8-460c-9563-55f204cf8221" ;
                dct:publisher
                    <http://data.brreg.no/enhetsregisteret/enhet/987654321> ;
                dct:provenance
                    <http://data.brreg.no/datakatalog/provinens/tredjepart> ;
                dcat:endpointDescription
                    <https://testdirektoratet.no/openapi/dataset/0.yaml> ;
                dct:spatial
                    <https://data.geonorge.no/administrativeEnheter/fylke/id/34> ;
                dct:subject
                    <https://testdirektoratet.no/model/concept/0> ,
                    <https://testdirektoratet.no/model/concept/1> ;
                foaf:page
                    <https://testdirektoratet.no> .

        <https://data.geonorge.no/administrativeEnheter/fylke/id/34>
                a               dct:Location;
                dct:identifier  "34";
                dct:title       "Innlandet" .

        <https://datasets.fellesdatakatalog.digdir.no/datasets/a1c680ca>
                a                  dcat:CatalogRecord ;
                dct:identifier     "a1c680ca" ;
                dct:issued         "2020-03-12T11:52:16.122Z"^^xsd:dateTime ;
                dct:modified       "2020-03-12T11:52:16.122Z"^^xsd:dateTime ;
                dct:modified       "2020-03-13"^^xsd:date ;
                foaf:primaryTopic  <https://testdirektoratet.no/model/dataset/0> ."""

    expected = b"""
        [
            {
                "identifier": ["adb4cf00-31c8-460c-9563-55f204cf8221"],
                "publisher": {
                "uri": "http://data.brreg.no/enhetsregisteret/enhet/987654321",
                "id": null,
                "name": null,
                "orgPath": null,
                "prefLabel": null,
                "organisasjonsform": null
                },
                "title": null,
                "description": null,
                "descriptionFormatted": null,
                "uri": "https://testdirektoratet.no/model/dataset/0",
                "accessRights": null,
                "themeUris": null,
                "theme": null,
                "losTheme": null,
                "eurovocThemes": null,
                "keyword": null,
                "contactPoint": null,
                "dctType": null,
                "issued": null,
                "modified": null,
                "landingPage": null,
                "language": null,
                "id": "a1c680ca",
                "harvest": {
                "firstHarvested": "2020-03-12T11:52:16Z",
                "changed": ["2020-03-12T11:52:16Z", "2020-03-13"]
                },
                "accessRightsComment": null,
                "distribution": null,
                "sample": null,
                "source": null,
                "objective": null,
                "page": ["https://testdirektoratet.no"],
                "admsIdentifier": null,
                "temporal": null,
                "subject": [
                {
                    "identifier": null,
                    "uri": "https://testdirektoratet.no/model/concept/0",
                    "prefLabel": null,
                    "definition": null
                },
                {
                    "identifier": null,
                    "uri": "https://testdirektoratet.no/model/concept/1",
                    "prefLabel": null,
                    "definition": null
                }
                ],
                "spatial": [
                {
                    "uri": "https://data.geonorge.no/administrativeEnheter/fylke/id/34",
                    "code": "34",
                    "prefLabel": { "nb": "Innlandet" }
                }
                ],
                "provenance": {
                "uri": "http://data.brreg.no/datakatalog/provinens/tredjepart",
                "code": null,
                "prefLabel": null
                },
                "accrualPeriodicity": {
                "uri": "http://publications.europa.eu/resource/authority/freq",
                "code": null,
                "prefLabel": null
                },
                "hasAccuracyAnnotation": null,
                "hasCompletenessAnnotation": null,
                "hasCurrentnessAnnotation": null,
                "hasAvailabilityAnnotation": null,
                "hasRelevanceAnnotation": null,
                "legalBasisForRestriction": null,
                "legalBasisForProcessing": null,
                "legalBasisForAccess": null,
                "conformsTo": null,
                "informationModel": null,
                "references": null,
                "qualifiedAttributions": null,
                "catalog": null,
                "isOpenData": false,
                "isAuthoritative": false,
                "isRelatedToTransportportal": false,
                "inSeries": null,
                "prev": null,
                "type": "datasets"
            }
        ]
        """

    parse_results = parse_rdf_to_classes(src, "datasets")
    result = convert_resources_to_json(parse_results)
    assert json.loads(result) == json.loads(expected)


@pytest.mark.unit
def test_invalid_rdf_fails_on_parse() -> None:
    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix xsd:   <http://www.w3.org/2001/XMLSchema#> .
        @prefix dcat:  <http://www.w3.org/ns/dcat#> .
        @prefix foaf:  <http://xmlns.com/foaf/0.1/> .

        <https://testdirektoratet.no/model/dataset/0>
                a                         dcat:Dataset ;
                dct:identifier
                    "adb4cf00-31c8-460c-9563-55f204cf8221" ;
                dct:publisher
                    <http://data.brreg.no/enhetsregisteret/enhet/987654321> ; # missing dot

        <https://datasets.fellesdatakatalog.digdir.no/datasets/a1c680ca>
                a                  dcat:CatalogRecord ;
                dct:identifier     "a1c680ca" ;
                dct:issued         "2020-03-12T11:52:16.122Z"^^xsd:dateTime ;
                dct:modified       "2020-03-12T11:52:16.122Z"^^xsd:dateTime ;
                dct:modified       "2020-03-13"^^xsd:date ;
                foaf:primaryTopic  <https://testdirektoratet.no/model/dataset/0> ."""

    with pytest.raises(Exception):
        parse_rdf_to_classes(src, "datasets")
