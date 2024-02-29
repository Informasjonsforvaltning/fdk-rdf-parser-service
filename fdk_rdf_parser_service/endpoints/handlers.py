"""Handler for parsing datasets"""
from aiohttp import web

from fdk_rdf_parser_service.service.service import parse_resource


async def handle_datasets(request: web.Request) -> web.Response:
    """Datasets route function. Parses datasets from RDF and returns them as JSON."""
    rdfData = await request.text()
    responseBody = parse_resource(rdfData, "datasets")
    return web.Response(body=responseBody, status=200, content_type="application/json")


async def handle_data_services(request: web.Request) -> web.Response:
    """Dataservices route function. Parses dataservices from RDF and returns them as JSON."""
    rdfData = await request.text()
    responseBody = parse_resource(rdfData, "data-services")
    return web.Response(body=responseBody, status=200, content_type="application/json")


async def handle_concepts(request: web.Request) -> web.Response:
    """Concepts route function. Parses concepts from RDF and returns them as JSON."""
    rdfData = await request.text()
    responseBody = parse_resource(rdfData, "concepts")
    return web.Response(body=responseBody, status=200, content_type="application/json")


async def handle_information_models(request: web.Request) -> web.Response:
    """Information model route function. Parses information models from RDF and returns them as JSON."""
    rdfData = await request.text()
    responseBody = parse_resource(rdfData, "information-models")
    return web.Response(body=responseBody, status=200, content_type="application/json")


async def handle_services(request: web.Request) -> web.Response:
    """Information model route function. Parses information models from RDF and returns them as JSON."""
    rdfData = await request.text()
    responseBody = parse_resource(rdfData, "services")
    return web.Response(body=responseBody, status=200, content_type="application/json")


async def handle_events(request: web.Request) -> web.Response:
    """Information model route function. Parses information models from RDF and returns them as JSON."""
    rdfData = await request.text()
    responseBody = parse_resource(rdfData, "events")
    return web.Response(body=responseBody, status=200, content_type="application/json")
