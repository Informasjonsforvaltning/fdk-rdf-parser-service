"""Resource module for liveness resources."""
from aiohttp import web

from fdk_rdf_parser_service.config import (
    rabbit_connection_key,
    rabbit_listen_channel_key,
)


async def ping(request: web.Request) -> web.Response:
    """Ping route function."""
    return web.Response(text="OK")


async def ready(request: web.Request) -> web.Response:
    """Ready route function. Checks connection to RabbitMQ."""
    connection = request.app[rabbit_connection_key]
    listen_channel = request.app[rabbit_listen_channel_key]
    if (
        connection
        and listen_channel
        and not connection.is_closed
        and not listen_channel.is_closed
    ):
        return web.Response(text="OK")
    else:
        return web.HTTPServiceUnavailable()
