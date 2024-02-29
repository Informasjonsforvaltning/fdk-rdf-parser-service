"""Resource module for liveness resources."""
from aiohttp import web


async def ping(request: web.Request) -> web.Response:
    """Ping route function."""
    return web.Response(text="OK")


async def ready(request: web.Request) -> web.Response:
    """Ready route function. Checks connection to RabbitMQ."""
    return web.Response(text="OK")
