"""Package for exposing validation endpoint and starting rabbit consumer."""
import logging

from aiohttp import web
from aiohttp_middlewares import cors_middleware, error_middleware
from fdk_rdf_parser_service.endpoints.handlers import (
    handle_concepts,
    handle_datasets,
    handle_data_services,
    handle_events,
    handle_information_models,
    handle_services,
)
from fdk_rdf_parser_service.endpoints import ping, ready
from fdk_rdf_parser_service.gunicorn_config import init_logger


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

    logging.info("Setting up app routes.")
    app.add_routes(
        [
            web.get("/ping", ping),
            web.get("/ready", ready),
            web.post("/datasets", handle_datasets),
            web.post("/data-services", handle_data_services),
            web.post("/concepts", handle_concepts),
            web.post("/information-models", handle_information_models),
            web.post("/services", handle_services),
            web.post("/events", handle_events),
        ]
    )

    return app
