"""Package for exposing validation endpoint."""
import logging

from aiohttp import web
from aiohttp_middlewares import cors_middleware, error_middleware

from fdk_rdf_parser_service.view import Ping, Ready


async def create_app() -> web.Application:
    """Create a web application."""
    logging.info("Creating app")

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

    return app


if __name__ == "__main__":
    web.run_app(create_app())
