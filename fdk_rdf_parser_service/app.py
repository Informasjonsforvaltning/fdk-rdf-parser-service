"""Package for exposing validation endpoint."""
import logging
import sys

from aiohttp import web
from aiohttp_middlewares import cors_middleware, error_middleware

from fdk_rdf_parser_service.config import (
    LOGGING_LEVEL,
    PingFilter,
    ReadyFilter,
    StackdriverJsonFormatter,
)
from fdk_rdf_parser_service.view import Ping, Ready


async def create_app() -> web.Application:
    """Create a web application."""
    logger = logging.getLogger()
    logger.setLevel(str(LOGGING_LEVEL))
    log_handler = logging.StreamHandler(sys.stdout)
    log_handler.setFormatter(StackdriverJsonFormatter())
    log_handler.addFilter(PingFilter())
    log_handler.addFilter(ReadyFilter())
    logger.addHandler(log_handler)

    logging.info("Creating web app.")
    app = web.Application(
        middlewares=[
            cors_middleware(allow_all=True),
            error_middleware(),  # default error handler for whole application
        ]
    )

    logging.info("Setting up ping and ready endpoints.")
    app.add_routes(
        [
            web.view("/ping", Ping),
            web.view("/ready", Ready),
        ]
    )

    logging.info("Creating rabbit listener.")

    return app


if __name__ == "__main__":
    web.run_app(create_app())
