from .base import *  # noqa: F403


class DevelopmentConfig:
    DEBUG = True
    ALLOWED_HOSTS = ["127.0.0.1", "localhost"]
    CORS_ORIGIN_WHITELIST = ["http://127.0.0.1:8000", "http://localhost:8000"]
    CORS_ALLOW_CREDENTIALS = True
