"""Rabbit MQ consumer."""
import asyncio
import logging

from aio_pika import connect, ExchangeType
from aio_pika.abc import AbstractConnection, AbstractIncomingMessage
from aiohttp import web

from fdk_rdf_parser_service.config import rabbit_connection_string, RABBITMQ
from fdk_rdf_parser_service.rabbit.parser_ingest import ingest_for_index


async def on_message(message: AbstractIncomingMessage) -> None:
    """On message received."""
    async with message.process():
        if message.routing_key is None:
            logging.error("routing key is None.")
        else:
            ingest_for_index(message.routing_key.split(".")[0], message.body)


async def close(app: web.Application) -> None:
    """Close Rabbit connections."""
    app["rabbit"]["listener"].cancel()
    await app["rabbit"]["listener"]
    await app["rabbit"]["connection"].close()


async def listen(app: web.Application) -> None:
    """Connect and listen."""
    exchange = RABBITMQ["EXCHANGE"]
    routing_key = RABBITMQ["LISTENER_ROUTING_KEY"]

    logging.info("Establishing RabbitMQ connection ...")
    connection: AbstractConnection = await connect(
        rabbit_connection_string(), loop=asyncio.get_event_loop()
    )

    logging.info("Establishing RabbitMQ channel ...")
    channel = await connection.channel()
    await channel.set_qos(prefetch_count=1)

    logging.info("RabbitMQ successfully connected to host.")

    topic_harvests_exchange = await channel.declare_exchange(
        exchange, ExchangeType.TOPIC
    )

    # Declaring anonymous queue
    queue = await channel.declare_queue(durable=False, exclusive=True, auto_delete=True)
    await queue.bind(topic_harvests_exchange, routing_key=routing_key)
    logging.info(f"RabbitMQ queue declared: {queue.name}")

    # Start listening
    app["rabbit"] = {
        "connection": connection,
        "listen_channel": channel,
        "listener": asyncio.create_task(queue.consume(on_message)),
    }
