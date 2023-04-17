"""."""
import asyncio
import logging

from aiohttp import web
from aiohttp_middlewares import cors_middleware, error_middleware

from .view import Ping, Ready


def create_parser_app():
    pass


async def create_parser_service():
    pass
