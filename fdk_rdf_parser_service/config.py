"""Project config."""

from os import environ as env
from typing import Dict

from dotenv import load_dotenv

import logging

load_dotenv()

LOGGING_LEVEL = env.get("LOGGING_LEVEL", "DEBUG")

HOST_PORT = env.get("HOST_PORT", "8000")

MONGO_DB: Dict[str, str] = {
    "HOST": env.get("DB_HOST", "http://localhost"),
    "PORT": env.get("DB_PORT", "27017"),
    "USERNAME": env.get("DB_USER", "admin"),
    "PASSWORD": env.get("DB_PASSWORD", "admin"),
}

RABBITMQ: Dict[str, str] = {
    "HOST": env.get("RABBIT_HOST"),
    "USERNAME": env.get("RABBIT_USERNAME"),
    "PASSWORD": env.get("RABBIT_PASSWORD"),
}

logging.basicConfig(level=LOGGING_LEVEL)
