import dataclasses
import datetime
import uuid
import simplejson
import logging
from typing import Any, Dict, List, Union

from aiohttp import ClientSession, web
from aiohttp.web_exceptions import HTTPError
from confluent_kafka import KafkaException
from confluent_kafka.schema_registry.avro import AvroSerializer
from confluent_kafka.serialization import (
    StringSerializer,
    SerializationContext,
    MessageField,
)

from fdk_rdf_parser import (
    parse_concepts,
    parse_data_services,
    parse_datasets,
    parse_events,
    parse_information_models,
    parse_public_services,
)


from fdk_rdf_parser.classes import (
    Concept,
    Dataset,
    DataService,
    Event,
    InformationModel,
    PublicService,
)

from fdk_rdf_parser_service import config
from fdk_rdf_parser_service.config import (
    RESOURCE_SERVICE_HOST,
    RESOURCE_SERVICE_API_KEY,
    REASONING_HOST,
)
from fdk_rdf_parser_service.kafka.producer import AIOProducer
from fdk_rdf_parser_service.model.parse_result import (
    ParsedCatalog,
    ParsedResource,
    RdfParseResult,
)
from fdk_rdf_parser_service.model.rabbit_report import FdkIdAndUri, RabbitReport
from fdk_rdf_parser_service.model.rdf_parse_event import (
    KafkaResourceType,
    RdfParseEvent,
)


async def handle_reports(app: web.Application, reports: List[RabbitReport]):
    """Handle reports."""
    results: List[RdfParseResult] = [
        await handle_report(report) for report in reports if not report.harvestError
    ]

    successful = [result for result in results if not result.report.harvestError]
    failed = [result for result in results if result.report.harvestError]
    logging.info(
        f"All reports handled. Successful: {len(successful)}, failed: {len(failed)}"
    )
    if failed:
        logging.info("Some reports failed.")
        for result in failed:
            logging.info(
                f"Failed report id: {result.report.id}, report url: {result.report.url}"
            )

    successful_post = await post_to_resource_service(successful)
    if successful_post:
        await send_kafka_messages(app, successful)
    else:
        logging.warning("Failed to post to resource service.")


async def handle_report(report: RabbitReport) -> RdfParseResult:
    """Handle catalogs in report."""
    parsed_catalogs = []
    for catalog in report.changedCatalogs:
        try:
            parsed_catalog = await fetch_and_parse_catalog(catalog, report.dataType)
            parsed_catalogs.append(parsed_catalog)
        except Exception as e:
            logging.warning(f"Failed to parse catalog {catalog.fdkId}: {e}")
            report.harvestError = True
    return RdfParseResult(parsedCatalogs=parsed_catalogs, report=report)


async def fetch_and_parse_catalog(
    catalog: FdkIdAndUri, catalogType: str
) -> ParsedCatalog:
    """Fetch and parse catalogs."""
    async with ClientSession() as session:
        rdf_data = await fetch_catalog(
            session, f"{REASONING_HOST}/{catalogType}/catalogs/{catalog.fdkId}"
        )
        parsed_resouces = parse_rdf_to_classes(rdf_data, catalogType)
        return ParsedCatalog(catalogId=catalog.fdkId, resources=parsed_resouces)


async def fetch_catalog(session: ClientSession, url: str) -> str:
    """Fetch catalog from reports."""
    async with session.get(url) as response:
        status = response.status
        if status != 200:
            logging.warning(f"Failed to fetch catalog {url}, status {status}")
        return await response.text()


def parse_rdf_to_classes(catalog_as_rdf: str, catalogType: str) -> List[ParsedResource]:
    """Parse RDF data to python classes."""
    parsed_resources: List[ParsedResource] = list()
    for fdkId, resource in parse_on_catalog_type(catalog_as_rdf, catalogType).items():
        parsed_resources.append(
            ParsedResource(
                fdkId=fdkId,
                resourceAsDict=dataclasses.asdict(resource),
                timestamp=datetime.datetime.now(datetime.timezone.utc),
            )
        )
    return parsed_resources


def convert_resources_to_json_list(resources: List[ParsedResource]) -> str:
    """Convert parsed resources to json."""
    return simplejson.dumps(
        [resource.resourceAsDict for resource in resources],
        iterable_as_array=True,
    )


def convert_resource_to_json(resourceAsDict: Dict[Any, Any]) -> str:
    return simplejson.dumps(resourceAsDict, iterable_as_array=True)


def parse_on_catalog_type(
    rdf_data: str, catalogType: str
) -> Dict[
    str,
    Union[
        Concept,
        Dataset,
        DataService,
        Event,
        InformationModel,
        PublicService,
    ],
]:
    parsers = {
        "concepts": parse_concepts,
        "dataservices": parse_data_services,
        "datasets": parse_datasets,
        "events": parse_events,
        "informationmodels": parse_information_models,
        "public_services": parse_public_services,
    }
    parser = parsers.get(catalogType)
    if parser:
        return parser(rdf_data)
    else:
        return dict()


async def send_kafka_messages(app: web.Application, results: List[RdfParseResult]):
    num_msg = [
        resource
        for result in results
        for catalog in result.parsedCatalogs
        for resource in catalog.resources
    ]
    logging.info(f"Sending {num_msg} messages to Kafka")
    kafka_producer = app[config.kafka_producer_key]
    avro_serializer = app[config.avro_serializer_key]
    string_serializer = app[config.string_serializer_key]
    for result in results:
        resource_type = get_resource_type(result.report.dataType)
        for parsed_catalog in result.parsedCatalogs:
            for parsed_resource in parsed_catalog.resources:
                event = RdfParseEvent(
                    resourceType=resource_type,
                    fdkId=parsed_resource.fdkId,
                    data=convert_resource_to_json(parsed_resource.resourceAsDict),
                    timestamp=parsed_resource.timestamp,
                )
                await send_kafka_message(
                    topic=config.KAFKA["TOPIC"],
                    kafka_producer=kafka_producer,
                    avro_serializer=avro_serializer,
                    string_serializer=string_serializer,
                    event=event,
                )


async def send_kafka_message(
    topic: str,
    kafka_producer: AIOProducer,
    avro_serializer: AvroSerializer,
    string_serializer: StringSerializer,
    event: RdfParseEvent,
):
    try:
        value = avro_serializer(
            event,
            SerializationContext(topic, MessageField.VALUE),
        )
        result = await kafka_producer.produce(
            topic=topic,
            key=string_serializer(str(uuid.uuid4())),
            value=value,
        )
        logging.debug(f"Successfully sent message: {result}")
    except KafkaException as e:
        logging.warning(
            f"Failed to send message to Kafka: {event.timestamp} {event.fdkId}"
        )
        logging.debug(
            f"Failed message data: {event.timestamp} {event.fdkId} {event.data}"
        )
        logging.debug(f"Kafka error: {e}")
        raise


def get_resource_type(catalogType: str) -> KafkaResourceType:
    resource_types: Dict[str, KafkaResourceType] = {
        "concepts": "CONCEPT",
        "dataservices": "DATASERVICE",
        "datasets": "DATASET",
        "events": "EVENT",
        "informationmodels": "INFORMATIONMODEL",
        "public_services": "SERVICE",
    }
    try:
        resource_type = resource_types[catalogType]
    except KeyError:
        raise ValueError(f"Unknown resource type: {catalogType}") from None
    return resource_type


async def post_to_resource_service(parse_results: List[RdfParseResult]):
    async def post(
        session: ClientSession, parsed_catalog: ParsedCatalog, catalogType: str
    ):
        try:
            body = convert_resources_to_json_list(parsed_catalog.resources)
            await session.post(
                f"{RESOURCE_SERVICE_HOST}/{catalogType}",
                data=body,
                headers={"X-API-KEY": RESOURCE_SERVICE_API_KEY},
            )
        except HTTPError as e:
            logging.warning(
                f"Failed to post to resource service. "
                f"catalogId: {parsed_catalog.catalogId} "
                f"err: {e}"
            )
            raise

    datatype_to_endpoint = {
        "concept": "concepts",
        "dataservice": "data-services",
        "dataset": "datasets",
        "event": "events",
        "informationmodel": "information-models",
        "publicServices": "services",
    }

    try:
        async with ClientSession() as session:
            for result in parse_results:
                catalogType = datatype_to_endpoint[result.report.dataType]
                for parsed_catalog in result.parsedCatalogs:
                    await post(session, parsed_catalog, catalogType)
        return True
    except HTTPError:
        return False
