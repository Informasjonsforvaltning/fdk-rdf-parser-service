"""Package for exposing validation endpoint and starting rabbit consumer."""


from fdk_rdf_parser_service import config

from fdk_rdf_parser_service.config import init_logger
from fdk_rdf_parser_service.kafka.producer import create_producer, get_produce_func
from fdk_rdf_parser_service.kafka.avro import setup_avro
from fdk_rdf_parser_service.kafka.consumer import create_and_subscribe_consumer, listen


def main() -> None:
    """Main function for service."""
    logger = init_logger()
    try:
        (avro_serializer, avro_deserializer, string_serializer) = setup_avro(
            schema_registry_url=config.KAFKA["SCHEMA_REGISTRY"],
            schema_path=config.KAFKA["SCHEMA_PATH"],
        )
        consumer = create_and_subscribe_consumer(
            config.kafka_consumer_config(), config.KAFKA["TOPIC"], logger
        )
        producer = create_producer(config.kafka_producer_config())
        produce_func = get_produce_func(
            producer, config.KAFKA["TOPIC"], avro_serializer, string_serializer
        )
        listen(consumer, avro_deserializer, produce_func)
    finally:
        consumer.close()
        producer.flush()
        producer.close()


if __name__ == "__main__":
    main()
