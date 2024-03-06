"""Package for exposing validation endpoint and starting rabbit consumer."""
from contextlib import asynccontextmanager
import logging
from fastapi import Body, Depends, FastAPI, HTTPException, Response, status
from fastapi.security.api_key import APIKey

import simplejson

from fdk_rdf_parser_service.auth import get_api_key
from fdk_rdf_parser_service.config import setup_logging

from fdk_rdf_parser_service.model import resource_type_map
from fdk_rdf_parser_service.service import parse_resource


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    logging.info("Starting app")
    yield


app = FastAPI(
    title="fdk-rdf-parser-service",
    description="Services that receives RDF graphs and parses them to JSON.",
    lifespan=lifespan,
)

API_KEY: APIKey = Depends(get_api_key)


@app.post(
    "/{resource_type}",
    response_model=None,
    description="Parses RDF data according to the given resource type and returns it as a JSON string",
    responses={
        200: {"description": "JSON response"},
        404: {"description": "Wrong resource type specified in the URL"},
        500: {"description": "Internal server error. Currently includes parse errors"},
    },
)
def handle_request(
    body: str = Body(..., media_type="text/turtle"),
    resource_type: str | None = None,
    api_key: APIKey = API_KEY,
) -> str:
    ensured_resource_type = (
        resource_type_map.get(resource_type) if resource_type else None
    )
    if ensured_resource_type is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    try:
        parsed_data = parse_resource(body, ensured_resource_type)
        return simplejson.dumps(parsed_data, iterable_as_array=True)
    except Exception as e:
        logging.debug(f"Failed to parse RDF graph: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@app.get("/ping")
def get_ping():
    """Ping route function."""
    return Response(content="OK", status_code=200)


@app.get("/ready")
def get_ready():
    """Ready route function."""
    return Response(content="OK", status_code=200)
