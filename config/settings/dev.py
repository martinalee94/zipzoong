from .base import *  # noqa: F403


class DevelopmentConfig:
    DEBUG = True
    ALLOWED_HOSTS = ["127.0.0.1", "localhost"]
