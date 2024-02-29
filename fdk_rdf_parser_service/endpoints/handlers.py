"""Handler for parsing datasets"""
from aiohttp import web

from fdk_rdf_parser_service.service.service import parse_resource


async def handle_datasets(request: web.Request) -> web.Response:
    """Datasets route function. Parses datasets from RDF and returns them as JSON."""
    rdfData = await request.text()
    responseBody = parse_resource(rdfData, "datasets")
    return web.Response(body=responseBody, status=200, content_type="application/json")
