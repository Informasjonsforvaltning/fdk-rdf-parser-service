"""Package for exposing validation endpoint and starting rabbit consumer."""
import logging

from aiohttp import web
from aiohttp_middlewares import cors_middleware, error_middleware
from fdk_rdf_parser_service.config import init_logger

from fdk_rdf_parser_service.endpoints import ping, ready


async def create_app() -> web.Application:
    """Create a web application."""
    logger = init_logger()
    logging.info("Creating web app.")
    app = web.Application(
        middlewares=[
            cors_middleware(allow_all=True),
            error_middleware(),  # default error handler for whole application
        ],
        logger=logger,
    )

    logging.info("Setting up ping and ready endpoints.")
    app.add_routes(
        [
            web.get("/ping", ping),
            web.get("/ready", ready),
        ]
    )

    return app
