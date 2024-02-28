from typing import Any, Callable, Dict
from confluent_kafka import Consumer, KafkaException
from confluent_kafka.schema_registry.avro import AvroDeserializer
from confluent_kafka.serialization import SerializationContext, MessageField
import logging

from fdk_rdf_parser_service.service.parser_service import handle_kafka_event


def create_and_subscribe_consumer(
    kafka_conf: Dict[str, str], kafka_topic: str, logger
) -> Consumer:
    consumer = Consumer(kafka_conf, logger)
    consumer.subscribe([kafka_topic])
    return consumer


def listen(
    consumer: Consumer,
    avro_deserializer: AvroDeserializer,
    produce_func: Callable[[Any], None],
):
    while True:
        try:
            msg = consumer.poll(timeout=1.0)
            if msg is None:
                continue

            value = avro_deserializer(
                msg.value(), SerializationContext(msg.topic(), MessageField.VALUE)
            )
            if value is not None:
                topic = msg.topic()
                partition = msg.partition()
                offset = msg.offset()
                key = msg.key()
                logging.debug(
                    f"Received message: {topic=} {partition=} {offset=} {key=} {value=}"
                )

            jsonData = handle_kafka_event(value.data, value.resourceType)

            # parsedEvent = RdfParseEvent(data=jsonData, resourceType=resourceType)
            # produce_func(event, uuid())

        except KafkaException as err:
            logging.warning(
                f"An error occured while listening to Kafka messages: {err}"
            )
            raise
