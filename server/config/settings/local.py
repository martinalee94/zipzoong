import os

from .base import *  # noqa: F403, F401

DEBUG = True
ALLOWED_HOSTS = ["127.0.0.1", "localhost", "0.0.0.0"]
CORS_ORIGIN_WHITELIST = ["http://127.0.0.1:8000", "http://localhost:8000"]
CORS_ALLOW_CREDENTIALS = True

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": os.getenv("LOCAL_DB_NAME"),
        "USER": os.getenv("LOCAL_DB_USER"),
        "PASSWORD": os.getenv("LOCAL_DB_PASSWORD"),
        "HOST": os.getenv("LOCAL_DB_HOST"),
        "PORT": os.getenv("LOCAL_DB_PORT"),
    }
}
