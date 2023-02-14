"""Rabbit M.Q. consumer."""
from typing import Dict

import aio_pika
from aiohttp import web

from .consumer import setup_rabbit_consumer
from .producer import setup_rabbit_producer


async def setup_rabbit(app: web.Application, rabbit_config: Dict[str, str]) -> None:
    """Setup shared connection to Rabbit broker."""
    username = rabbit_config["USERNAME"]
    password = rabbit_config["PASSWORD"]
    host = rabbit_config["HOST"]

    connection_string = f"amqp://{username}:{password}@{host}"

    app["fdk.rabbit.connection"] = await aio_pika.connect(connection_string)

    await setup_rabbit_producer(app)
    await setup_rabbit_consumer(app)
