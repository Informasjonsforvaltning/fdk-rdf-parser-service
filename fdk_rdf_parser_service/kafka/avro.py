from aiohttp import web
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer
from confluent_kafka.serialization import StringSerializer
from fdk_rdf_parser_service import config


async def setup_avro(app: web.Application):
    schema_path = config.KAFKA["SCHEMA_PATH"]
    with open(f"{schema_path}") as f:
        schema_str = f.read()

    schema_registry_conf = {"url": config.KAFKA["SCHEMA_REGISTRY"]}
    schema_registry_client = SchemaRegistryClient(schema_registry_conf)

    app["kafka"] = dict()
    app["kafka"]["avro_serializer"] = AvroSerializer(schema_registry_client, schema_str)
    app["kafka"]["string_serializer"] = StringSerializer("utf_8")
