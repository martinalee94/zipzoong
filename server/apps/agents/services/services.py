from pathlib import Path
from random import randrange

from apps.commons.exceptions import (
    APIException,
    APIExceptionErrorCodes,
    ImageSizeIsExceeded,
    ImageTypeIsNotAllowed,
)
from apps.commons.utils import ALLOWED_IMAGE_SIZE, ALLOWED_IMAGE_TYPE
from apps.users.utils import AgentToken
from config.settings.base import MEDIA_ROOT
from PIL import Image

from ..domains.models import Agent, AgentImage
from . import exceptions


def add_new_agent(email, password, confirmed_password, name):
    agent = Agent.objects.filter(email=email).first()
    if agent:
        raise exceptions.AgentAlreadyExist
    if password != confirmed_password:
        raise exceptions.PasswordCheckRequired

    agent = Agent(email=email, password=password, name=name)
    agent.save()
    return


def issue_agent_access_token(email, password, **kwargs):
    token = AgentToken(email=email, password=password).encode()
    return {"email": email, "access_token": token}


def update_agent_detail(decoded_token, position, association, license_num):
    email = decoded_token["email"]
    agent = Agent.objects.filter(email=email).first()
    if not agent:
        raise exceptions.AgentDoesNotExist
    agent.association = association
    agent.position = position
    agent.license_num = license_num
    agent.save()
    return


def add_agent_license_images(decoded_token, image, file_date_key):
    email = decoded_token["email"]
    agent = Agent.objects.filter(email=email).first()
    if not agent:
        raise exceptions.AgentDoesNotExist
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

        Path(MEDIA_ROOT + f"/{agent.id}/{file_date_key}").mkdir(parents=True, exist_ok=True)
        rest_of_path = f"/{agent.id}/{file_date_key}/{file_name_key}.png"
        path = MEDIA_ROOT + rest_of_path

        origin_image.save(path, "PNG")

        image = AgentImage(
            agent=agent,
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
