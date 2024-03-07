"""Package for exposing validation endpoint and starting rabbit consumer."""
from contextlib import asynccontextmanager
import logging
from fastapi import Body, FastAPI, HTTPException, Response, status
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


@app.get("/ping")
def get_ping():
    """Ping route function."""
    return Response(content="OK", status_code=200)


@app.get("/ready")
def get_ready():
    """Ready route function."""
    return Response(content="OK", status_code=200)


@app.post("/{resource_type}")
def handle_request(
    body: str = Body(..., media_type="text/turtle"), resource_type: str | None = None
):
    ensured_resource_type = (
        resource_type_map.get(resource_type) if resource_type else None
    )
    if ensured_resource_type is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    try:
        parsed_data = parse_resource(body, ensured_resource_type)
        return parsed_data
    except Exception as e:
        logging.debug(f"Failed to parse RDF graph: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
