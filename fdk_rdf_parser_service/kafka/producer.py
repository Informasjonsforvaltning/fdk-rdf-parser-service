import logging
from typing import Any, Callable, Dict
from uuid import uuid4
from confluent_kafka import Producer
from confluent_kafka.schema_registry.avro import AvroSerializer
from confluent_kafka.serialization import SerializationContext, MessageField
from confluent_kafka.serialization import StringSerializer


def create_producer(kafka_conf: Dict[str, str]) -> Producer:
    return Producer(kafka_conf)


def get_produce_func(
    producer: Producer,
    kafka_topic: str,
    avro_serializer: AvroSerializer,
    string_serializer: StringSerializer,
) -> Callable[[Any], None]:
    def produce(value: Any):
        producer.produce(
            topic=kafka_topic,
            key=string_serializer(str(uuid4())),
            value=avro_serializer(
                value, SerializationContext(kafka_topic, MessageField.VALUE)
            ),
            on_delivery=delivery_report,
        )

    return produce


def delivery_report(err, msg):
    if err is not None:
        logging.info(f"Delivery failed for User record {msg.key}: {err}")
        return
    logging.info(
        f"Value {msg.key()} successfully produced to {msg.topic()} [{msg.partition()}] at offset {msg.offset()}"
    )
