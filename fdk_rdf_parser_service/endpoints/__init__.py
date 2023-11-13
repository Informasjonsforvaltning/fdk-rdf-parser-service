"""Package for endpoints."""
from .liveness import ping, ready

__all__ = ["ping", "ready"]
