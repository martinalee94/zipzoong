import os

from .base import *  # noqa: F403

DEBUG = False
ALLOWED_HOSTS = ["localhost"]  # TODO: 추후 서버 주소 추가 필요

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
