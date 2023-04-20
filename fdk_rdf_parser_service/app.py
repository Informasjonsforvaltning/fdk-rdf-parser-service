"""Package for exposing validation endpoint and starting rabbit consumer."""
import asyncio
from contextlib import suppress
import logging
from typing import AsyncIterator

from aiohttp import web
from aiohttp_middlewares import cors_middleware, error_middleware

from fdk_rdf_parser_service.config import init_logger
from fdk_rdf_parser_service.rabbit.consumer.consumer import start_rabbit_listener
from fdk_rdf_parser_service.view import Ping, Ready


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
            web.view("/ping", Ping),
            web.view("/ready", Ready),
        ]
    )

    app.cleanup_ctx.append(background_tasks)

    logging.info("Setup finished.")
    return app


async def background_tasks(app: web.Application) -> AsyncIterator:
    """Background tasks for web app."""
    logging.info("Starting rabbit listener.")
    app["rabbit_listener"] = asyncio.create_task(start_rabbit_listener())

    logging.info("Yielding")
    yield

    logging.info("Cancelling rabbit_listener")
    app["rabbit_listener"].cancel()
    with suppress(asyncio.CancelledError):
        await app["rabbit_listener"]


def main() -> None:
    """Main function for service."""
    try:
        web.run_app(create_app())
    except Exception as e:
        logging.error(f"Exception in main: {e}")
        raise SystemExit() from e


if __name__ == "__main__":
    main()
