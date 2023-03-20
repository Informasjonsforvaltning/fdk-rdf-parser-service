"""Package for exposing validation endpoint."""

from aiohttp import web
from aiohttp_middlewares import cors_middleware, error_middleware

from fdk_rdf_parser_service.config import RABBITMQ

from .rabbit import setup_rabbit
from .view import Ping, Ready


async def create_app() -> web.Application:
    """Create a web application."""
    app = web.Application(
        middlewares=[
            cors_middleware(allow_all=True),
            error_middleware(),  # default error handler for whole application
        ]
    )
    app.add_routes(
        [
            web.view("/ping", Ping),
            web.view("/ready", Ready),
        ]
    )

    await setup_rabbit(app=app, rabbit_config=RABBITMQ)

    return app
