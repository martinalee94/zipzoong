from .base import *  # noqa: F403


class ProductionConfig:
    DEBUG = False
    ALLOWED_HOSTS = ["localhost"]  # TODO: 추후 서버 주소 추가 필요
