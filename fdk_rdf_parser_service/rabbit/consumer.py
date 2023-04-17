"""Rabbit M.Q. consumer."""
import asyncio
import logging
import sys
from typing import Any

import pika
from pika.exchange_type import ExchangeType

from fdk_rdf_parser_service.config import RABBITMQ


def create_rabbit_consumer() -> None:
    """Connect and listen to Rabbit queue."""
    logging.debug("Setting up rabbit consumer.")

    username = RABBITMQ["USERNAME"]
    password = RABBITMQ["PASSWORD"]
    host = RABBITMQ["HOST"]

    credentials = pika.PlainCredentials(username=username, password=password)
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host, credentials=credentials)
    )

    channel = connection.channel()
    channel.basic_qos(prefetch_count=1)

    channel.exchange_declare("harvests", ExchangeType.topic)

    channel.queue_declare(
        durable=False,
        exclusive=True,
        auto_delete=True,
        # queue="fdk-rdf-parser-service",
        queue="",
    )

    channel.queue_bind(
        exchange="harvests",
        # queue="fdk-rdf-parser-service",
        routing_key="*.reasoned",
    )

    channel.basic_consume(
        # queue="fdk-rdf-parser-service",
        queue="",
        auto_ack=True,
        on_message_callback=on_message,
    )

    try:
        logging.info("Waiting for messages")
        channel.start_consuming()
    finally:
        logging.warning("Closing channel and connection")
        channel.close()
        connection.close()


def on_message(
    ch: pika.channel.Channel,
    method: pika.spec.Basic.Deliver,
    properties: pika.spec.BasicProperties,
    body: bytes,
) -> Any:
    """Rabbit message handler."""
    logging.info(f"Message received. Routing key {str(method.routing_key)}")
    # requests.post("localhost:port", body)
    # if (routing_key == concepts)
    # requests.post("localhost:port/concepts", body)


if __name__ == "__main__":
    try:
        create_rabbit_consumer()
    except Exception as e:
        logging.exception(e)
