"""Package for exposing validation endpoint and starting rabbit consumer."""

from contextlib import asynccontextmanager
import logging

from fastapi import Body, Depends, FastAPI, HTTPException, status
from fastapi.security.api_key import APIKey

from fdk_rdf_parser.classes.exceptions import (
    MissingResourceError,
    MultipleResourcesError,
    ParserError,
)

from fdk_rdf_parser_service.auth import get_api_key
from fdk_rdf_parser_service.config import setup_logging

from fdk_rdf_parser_service.model import resource_type_map
from fdk_rdf_parser_service.service import ParsedReturnType, parse_resource


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    logging.info("Starting app")
    yield


app = FastAPI(
    title="fdk-rdf-parser-service",
    description="Services that receives RDF graphs and parses them to JSON.",
    lifespan=lifespan,
    version="0.1.0",
)

API_KEY: APIKey = Depends(get_api_key)


@app.post(
    "/{resource_type}",
    response_model=None,
    description="Parses RDF data according to the given resource type and returns it as a JSON string",
    responses={
        200: {"description": "JSON response."},
        400: {
            "description": "Bad request, bad input data.",
        },
        401: {
            "description": "Unauthorized, missing or invalid API key.",
        },
        404: {
            "description": "Wrong resource type specified in the URL.",
        },
        500: {
            "description": "Internal server error.",
        },
    },
)
def handle_request(
    body: str = Body(..., media_type="text/turtle"),
    resource_type: str | None = None,
    api_key: APIKey = API_KEY,
) -> ParsedReturnType | HTTPException:
    ensured_resource_type = (
        resource_type_map.get(resource_type) if resource_type else None
    )
    if ensured_resource_type is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    try:
        parsed_data = parse_resource(body, ensured_resource_type)
        return parsed_data
    except (ParserError, MissingResourceError, MultipleResourcesError) as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(err)
        ) from err
    except Exception as e:
        logging.error(f"Severe failure occured during parsing: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str("Severe error in service."),
        ) from None


@app.get("/ping")
def get_ping() -> str:
    """Ping route function."""
    return "OK"


@app.get("/ready")
def get_ready() -> str:
    """Ready route function."""
    return "OK"
