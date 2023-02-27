"""Project config."""

from os import environ as env
from typing import Dict

from dotenv import load_dotenv

load_dotenv()

LOGGING_LEVEL = env.get("LOGGING_LEVEL", "INFO")

HOST_PORT = env.get("HOST_PORT", "8000")

RABBITMQ: Dict[str, str] = {
    "HOST": env.get("RABBIT_HOST", "localhost"),
    "USERNAME": env.get("RABBIT_USERNAME", "admin"),
    "PASSWORD": env.get("RABBIT_PASSWORD", "admin"),
}

MONGO_DB: Dict[str, str] = {
    "HOST": env.get("DB_HOST", "http://localhost"),
    "PORT": env.get("DB_PORT", "27017"),
    "USERNAME": env.get("DB_USER", "admin"),
    "PASSWORD": env.get("DB_PASSWORD", "admin"),
}
