"""Resource module for liveness resources."""
from aiohttp import web


async def ping(request: web.Request) -> web.Response:
    """Ping route function."""
    return web.Response(text="OK")


async def ready(request: web.Request) -> web.Response:
    """Ready route function. Checks connection to RabbitMQ."""
    connection = request.app["rabbit"]["connection"]
    listen_channel = request.app["rabbit"]["listen_channel"]
    if (
        connection
        and listen_channel
        and not connection.is_closed
        and not listen_channel.is_closed
    ):
        return web.Response(text="OK")
    else:
        return web.HTTPServiceUnavailable()
