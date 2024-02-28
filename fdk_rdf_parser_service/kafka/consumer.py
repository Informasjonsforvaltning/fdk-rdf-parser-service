from typing import Dict, List
from confluent_kafka import Consumer, KafkaException
from confluent_kafka.schema_registry.avro import AvroDeserializer
from confluent_kafka.serialization import SerializationContext, MessageField
import logging


def create_and_subscribe_consumer(
    kafka_config: Dict[str, str], kafka_topics: List[str], logger
) -> Consumer:
    consumer = Consumer(kafka_config, logger)
    consumer.subscribe(kafka_topics)
    return consumer


def listen(consumer: Consumer, avro_deserializer: AvroDeserializer):
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
        except KafkaException as err:
            logging.warning(
                f"An error occured while listening to Kafka messages: {err}"
            )
            raise
        finally:
            consumer.close()
