"""Package for exposing validation endpoint and starting rabbit consumer."""
import logging

from aiohttp import web
from aiohttp_middlewares import cors_middleware, error_middleware

from fdk_rdf_parser_service.config import init_logger
from fdk_rdf_parser_service.endpoints import ping, ready
from fdk_rdf_parser_service.rabbit import consumer


async def create_app(logger: logging.Logger) -> web.Application:
    """Create a web application."""
    logging.info("Creating web app.")
    app = web.Application(
        middlewares=[
            cors_middleware(allow_all=True),
            error_middleware(),  # default error handler for whole application
        ],
        logger=logger,
    )

    app.on_startup.append(consumer.listen)
    app.on_cleanup.append(consumer.close)

    logging.info("Setting up ping and ready endpoints.")
    app.add_routes(
        [
            web.get("/ping", ping),
            web.get("/ready", ready),
        ]
    )

    logging.info("Setup finished.")
    return app


def main() -> None:
    """Main function for service."""
    logger = init_logger()
    try:
        web.run_app(create_app(logger), print=logger.debug)
    except Exception as e:
        logging.error(f"Exception in main: {e}")
        raise


if __name__ == "__main__":
    main()
