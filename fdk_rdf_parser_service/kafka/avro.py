from typing import Tuple
from aiohttp.web import Application
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer, AvroDeserializer
from confluent_kafka.serialization import StringSerializer


async def setup_avro_old(app: Application):
    pass


def setup_avro(
    schema_registry_url, schema_path
) -> Tuple[AvroSerializer, AvroDeserializer, StringSerializer]:
    schema_registry_conf = {"url": schema_registry_url}
    schema_registry_client = SchemaRegistryClient(schema_registry_conf)
    with open(f"{schema_path}") as f:
        schema_str = f.read()
    avro_serializer = AvroSerializer(schema_registry_client, schema_str)
    avro_deserializer = AvroDeserializer(schema_registry_client, schema_str)
    string_serializer = StringSerializer("utf_8")
    return (avro_serializer, avro_deserializer, string_serializer)
