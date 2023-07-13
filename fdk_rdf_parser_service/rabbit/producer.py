"""Rabbit M.Q. producer."""

from aiohttp import web


async def publish_parser_report(
    app: web.Application, success: bool = True, msg: str | None = None
) -> None:
    """Placeholder for setting up rabbit_producer."""
    pass
