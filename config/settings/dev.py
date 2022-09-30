import os

from .base import *  # noqa: F403

DEBUG = True
ALLOWED_HOSTS = ["127.0.0.1", "localhost"]
CORS_ORIGIN_WHITELIST = ["http://127.0.0.1:8000", "http://localhost:8000"]
CORS_ALLOW_CREDENTIALS = True

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": os.getenv("DEV_DB_NAME"),
        "USER": os.getenv("DEV_DB_USER"),
        "PASSWORD": os.getenv("DEV_DB_PASSWORD"),
        "HOST": os.getenv("DEV_DB_HOST"),
        "PORT": os.getenv("DEV_DB_PORT"),
    }
}
