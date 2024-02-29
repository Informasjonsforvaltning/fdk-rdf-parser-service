"""Handler for parsing resources from rdfData to JSON"""
from aiohttp import web

from fdk_rdf_parser_service.service.service import parse_resource


async def handle_datasets(request: web.Request) -> web.Response:
    rdfData = await request.text()
    responseBody = parse_resource(rdfData, "datasets")
    return web.Response(body=responseBody, status=200, content_type="application/json")


async def handle_data_services(request: web.Request) -> web.Response:
    rdfData = await request.text()
    responseBody = parse_resource(rdfData, "data-services")
    return web.Response(body=responseBody, status=200, content_type="application/json")


async def handle_concepts(request: web.Request) -> web.Response:
    rdfData = await request.text()
    responseBody = parse_resource(rdfData, "concepts")
    return web.Response(body=responseBody, status=200, content_type="application/json")


async def handle_information_models(request: web.Request) -> web.Response:
    rdfData = await request.text()
    responseBody = parse_resource(rdfData, "information-models")
    return web.Response(body=responseBody, status=200, content_type="application/json")


async def handle_services(request: web.Request) -> web.Response:
    rdfData = await request.text()
    responseBody = parse_resource(rdfData, "services")
    return web.Response(body=responseBody, status=200, content_type="application/json")


async def handle_events(request: web.Request) -> web.Response:
    rdfData = await request.text()
    responseBody = parse_resource(rdfData, "events")
    return web.Response(body=responseBody, status=200, content_type="application/json")
