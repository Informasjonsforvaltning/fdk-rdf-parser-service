"""Rabbit MQ consumer."""
import asyncio
import json
import logging
from typing import List

from aio_pika import connect, ExchangeType
from aio_pika.abc import AbstractConnection, AbstractIncomingMessage
from aiohttp import web

from fdk_rdf_parser_service.config import (
    rabbit_connection_string,
    rabbit_connection_key,
    rabbit_listen_channel_key,
    rabbit_listener_key,
    RABBITMQ,
)
from fdk_rdf_parser_service.model.rabbit_report import RabbitReport
from fdk_rdf_parser_service.service.parser_service import handle_reports


async def on_message(message: AbstractIncomingMessage) -> None:
    """On message received."""
    async with message.process():
        await read_reasoned_message(message.body)


async def close(app: web.Application) -> None:
    """Close Rabbit connections."""
    await app[rabbit_listen_channel_key].close()


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
    app[rabbit_connection_key] = connection
    app[rabbit_listen_channel_key] = channel
    app[rabbit_listener_key] = asyncio.create_task(queue.consume(on_message))


async def read_reasoned_message(body: bytes):
    """Read message and reports."""
    try:
        reports = parse_json_body_reports_list(body)
        logging.info(f"Received {len(reports)} reports.")
        for report in reports:
            logging.info(
                f"Report id: {report.id}"
                f"Report url: {report.url}"
                f"startTime: {report.startTime}"
                f"endTime: {report.endTime}"
                f"changedCatalogs: {len(report.changedCatalogs)}"
                f"changedResources: {len(report.changedResources)}"
            )
        await handle_reports(reports)

    except Exception as err:
        logging.error(f"Error when reading rabbit messages: {err}", exc_info=True)


def parse_json_body_reports_list(body: bytes) -> List[RabbitReport]:
    """Parse JSON body with list of reports."""
    return [RabbitReport.from_json(json.dumps(report)) for report in json.loads(body)]
