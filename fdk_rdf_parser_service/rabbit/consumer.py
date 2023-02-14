"""Rabbit M.Q. consumer."""
import asyncio
import logging
from typing import Any

import aio_pika
from aiohttp import web


async def setup_rabbit_consumer(app: web.Application) -> None:
    """Connect and listen to Rabbit queue."""
    logging.debug("Setting up rabbit consumer.")

    listen_channel = await app["fdk.rabbit.connection"].channel()
    await listen_channel.set_qos(prefetch_count=1)

    topic_harvests_exchange = await listen_channel.declare_exchange(
        "harvests", aio_pika.ExchangeType.TOPIC
    )

    queue = await listen_channel.declare_queue(
        durable=False, exclusive=True, auto_delete=True
    )
    await queue.bind(topic_harvests_exchange, routing_key="*.reasoned")

    app["fdk.rabbit.listener"] = asyncio.create_task(queue.consume(on_message))


async def on_message(message: aio_pika.IncomingMessage) -> Any:
    """Rabbit message handler."""
    logging.info("Rabbit message received.")
