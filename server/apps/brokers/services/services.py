from pathlib import Path
from random import randrange

from apps.commons.exceptions import (
    APIException,
    APIExceptionErrorCodes,
    ImageSizeIsExceeded,
    ImageTypeIsNotAllowed,
)
from apps.commons.utils import ALLOWED_IMAGE_SIZE, ALLOWED_IMAGE_TYPE
from apps.users.utils import BrokerToken
from config.settings.base import MEDIA_ROOT
from PIL import Image

from ..domains.models import Broker, BrokerImage
from . import exceptions


def add_new_broker(email, password, confirmed_password, name):
    broker = Broker.objects.filter(email=email).first()
    if broker:
        raise exceptions.BrokerAlreadyExist
    if password != confirmed_password:
        raise exceptions.PasswordCheckRequired

    broker = Broker(email=email, password=password, name=name)
    broker.save()
    return


def issue_broker_access_token(email, password, **kwargs):
    token = BrokerToken(email=email, password=password).encode()
    return {"email": email, "access_token": token}


def update_broker_detail(decoded_token, position, association, license_num):
    email = decoded_token["email"]
    broker = Broker.objects.filter(email=email).first()
    if not broker:
        raise exceptions.BrokerDoesNotExist
    broker.association = association
    broker.position = position
    broker.license_num = license_num
    broker.save()
    return


def add_broker_license_images(decoded_token, image, file_date_key):
    email = decoded_token["email"]
    broker = Broker.objects.filter(email=email).first()
    if not broker:
        raise exceptions.BrokerDoesNotExist
    try:
        if image.size > ALLOWED_IMAGE_SIZE:
            raise ImageSizeIsExceeded

        origin_image_type = image.name.split(".")[-1].lower()
        if origin_image_type not in ALLOWED_IMAGE_TYPE:
            raise ImageTypeIsNotAllowed

        # 파일이름 "houseid_filedatekey_filenamekey"
        file_name_key = randrange(10000000, 99999999)

        origin_image = Image.open(image)
        origin_width, origin_height = origin_image.size

        Path(MEDIA_ROOT + f"/{broker.id}/{file_date_key}").mkdir(parents=True, exist_ok=True)
        rest_of_path = f"/{broker.id}/{file_date_key}/{file_name_key}.png"
        path = MEDIA_ROOT + rest_of_path

        origin_image.save(path, "PNG")

        image = BrokerImage(
            broker=broker,
            path=path,
            name=f"{file_name_key}.png",
            type="png",
            size=image.size,
            width=origin_width,
            height=origin_height,
        )
        image.save()
        return
    except ImageSizeIsExceeded:
        raise APIException(APIExceptionErrorCodes.BAD_REQUEST, message="Image is too big")
    except ImageTypeIsNotAllowed:
        raise APIException(
            APIExceptionErrorCodes.BAD_REQUEST,
            message="File type is not allowed - (jpg, jpeg, png)",
        )
    return
