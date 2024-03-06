"""Package for exposing validation endpoint and starting rabbit consumer."""
from contextlib import asynccontextmanager
import logging
from fastapi import Body, FastAPI, HTTPException, Response, status
import simplejson
from fdk_rdf_parser_service.config import setup_logging

from fdk_rdf_parser_service.model import catalog_type_map
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


@app.post("/{catalog_type}")
def handle_request(
    body: str = Body(..., media_type="text/turtle"), catalog_type: str | None = None
):
    ensured_catalog_type = catalog_type_map.get(catalog_type) if catalog_type else None
    if ensured_catalog_type is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    try:
        parsed_data = parse_resource(body, ensured_catalog_type)
        return simplejson.dumps(parsed_data, iterable_as_array=True)
    except Exception as e:
        logging.debug(f"Failed to parse RDF graph: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
