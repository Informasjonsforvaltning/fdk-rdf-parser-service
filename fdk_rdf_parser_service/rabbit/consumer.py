"""Rabbit M.Q. consumer."""
import logging
from typing import Any

import aio_pika
from aiohttp import web


async def setup_rabbit_consumer(app: web.Application) -> None:
    """Connect and listen to Rabbit queue."""
    logging.debug("Setting up rabbit consumer.")

    connection = app["fdk.rabbit.connection"]

    async with connection:
        listen_channel = await connection.channel()

        await listen_channel.set_qos(prefetch_count=1)

        topic_harvests_exchange = await listen_channel.declare_exchange(
            "harvests", aio_pika.ExchangeType.TOPIC
        )

        queue = await listen_channel.declare_queue(
            durable=False,
            exclusive=True,
            auto_delete=True,
            name="fdk-rdf-parser-service",
        )
        await queue.bind(topic_harvests_exchange, routing_key="*.reasoned")

        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                await on_message(message)


async def on_message(message: aio_pika.IncomingMessage) -> Any:
    """Rabbit message handler."""
    async with message.process():
        logging.info("Rabbit message received")