import random
import string
from datetime import datetime
from pathlib import Path
from random import randrange

from apps.commons.exceptions import (
    APIException,
    APIExceptionErrorCodes,
    ImageSizeIsExceeded,
    ImageTypeIsNotAllowed,
)
from apps.commons.utils import ALLOWED_IMAGE_SIZE, ALLOWED_IMAGE_TYPE
from apps.houses.apis import schemas as house_schemas
from apps.houses.domains.models import House, HouseBidInfo, HouseImage
from apps.houses.services.enums import ContractTypes
from apps.users.domains.models import Notice, Qna
from apps.users.utils import AgentToken
from config.settings.base import MEDIA_ROOT
from django.core.paginator import Paginator
from PIL import Image

from ..domains.models import Agent, AgentImage
from . import exceptions


def create_agent_id():
    chars = string.ascii_uppercase + string.digits
    return "a-" + "".join(random.choice(chars) for _ in range(10))


def add_new_agent(email, password, confirmed_password, name):
    agent = Agent.objects.filter(email=email).first()
    if agent:
        raise exceptions.AgentAlreadyExist
    if password != confirmed_password:
        raise exceptions.PasswordCheckRequired

    agent_id = create_agent_id()
    agent = Agent(id=agent_id, email=email, password=password, name=name)
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


def get_nearby_houses_list(
    decoded_token, location: str, pagination: house_schemas.PaginationListSchema
):
    email = decoded_token["email"]
    agent = Agent.objects.filter(email=email).first()
    if not agent:
        raise exceptions.AgentDoesNotExist

    houses = House.objects.filter(dong_addr__contains=location).prefetch_related("detail")
    houses.order_by("created_dt")
    houses = Paginator(houses, pagination.info_num).page(pagination.page_num).object_list

    result = []
    for house in houses:
        house_dict = {}
        options = {
            "type": house.detail.type_option,
            "floor": house.detail.floor_option,
            "room": house.detail.rooms_option,
            "restroom": house.detail.restroom_option,
            "duplex": house.detail.duplex_option,
        }

        contract_detail = {}
        if house.contract_type == ContractTypes.SALE:
            contract_detail["sale_price"] = house.sale_price
        elif house.contract_type == ContractTypes.CHARTERED_RENT:
            contract_detail["charter_rent"] = house.charter_rent
        elif house.contract_type == ContractTypes.MONTHLY_RENT:
            contract_detail["monthly_deposit"] = house.monthly_deposit
            contract_detail["monthly_rent"] = house.monthly_rent

        images_list = []
        images = HouseImage.objects.filter(house=house)
        for image in images:
            img = {}
            img["path"] = image.path
            img["name"] = image.name
            images_list.append(img)

        house_dict["id"] = house.id
        house_dict["address"] = house.full_street_addr
        house_dict["contract_type"] = house.contract_type
        house_dict["contract_detail"] = contract_detail
        house_dict["options"] = options
        house_dict["images"] = images_list
        result.append(house_dict)

    return result


def add_agent_biding_info(decoded_token, house_id, bid_price):
    email = decoded_token["email"]
    agent = Agent.objects.filter(email=email).first()
    if not agent:
        raise exceptions.AgentDoesNotExist

    house_bid = HouseBidInfo.objects.filter(house_id=house_id, agent_id=agent.id).first()
    if house_bid:
        house_bid.bid_price = bid_price
        house_bid.save()
    else:
        HouseBidInfo.objects.create(house_id=house_id, agent_id=agent.id, bid_price=bid_price)
    return


def add_agent_profile_image(decoded_token: str, upload_image):
    email = decoded_token["email"]
    agent = Agent.objects.filter(email=email).first()
    if not agent:
        raise exceptions.AgentDoesNotExist

    pillow_image = Image.open(upload_image)
    width, height = pillow_image.size
    file_date_key = datetime.now().strftime("%Y%m%d_%H%M%S")
    Path(MEDIA_ROOT + f"/{agent.id}").mkdir(parents=True, exist_ok=True)
    path = MEDIA_ROOT + f"/{agent.id}/{file_date_key}.png"
    pillow_image.save(path, "PNG")

    image = AgentImage.objects.filter(agent=agent).first()
    if image:
        image.path = path
        image.name = f"{file_date_key}.png"
        image.size = upload_image.size
        image.width = width
        image.height = height
        image.save()
    else:
        image = AgentImage(
            agent=agent,
            path=path,
            name=f"{file_date_key}.png",
            type="png",
            size=upload_image.size,
            width=width,
            height=height,
        )
        image.save()
    return


def get_agent_profile(decoded_token):
    email = decoded_token["email"]
    agent = Agent.objects.filter(email=email).first()
    if not agent:
        raise exceptions.AgentDoesNotExist

    image = AgentImage.objects.get(agent=agent)
    return (email, image)


def get_biding_house_list(decoded_token, pagination):
    email = decoded_token["email"]
    agent = Agent.objects.filter(email=email).first()
    if not agent:
        raise exceptions.AgentDoesNotExist

    house_bids = HouseBidInfo.objects.filter(agent__id=agent.id)
    house_bids.order_by("created_dt")
    house_bids = Paginator(house_bids, pagination.info_num).page(pagination.page_num).object_list

    result = []
    for bid in house_bids:
        house_dict = {}

        options = {
            "type": bid.house.detail.type_option,
            "floor": bid.house.detail.floor_option,
            "room": bid.house.detail.rooms_option,
            "restroom": bid.house.detail.restroom_option,
            "duplex": bid.house.detail.duplex_option,
        }

        contract_detail = {}
        if bid.house.contract_type == ContractTypes.SALE:
            contract_detail["sale_price"] = bid.house.sale_price
        elif bid.house.contract_type == ContractTypes.CHARTERED_RENT:
            contract_detail["charter_rent"] = bid.house.charter_rent
        elif bid.house.contract_type == ContractTypes.MONTHLY_RENT:
            contract_detail["monthly_deposit"] = bid.house.monthly_deposit
            contract_detail["monthly_rent"] = bid.house.monthly_rent

        images_list = []
        images = HouseImage.objects.filter(house_id=bid.house.id)
        for image in images:
            img = {}
            img["path"] = image.path
            img["name"] = image.name
            images_list.append(img)

        house_dict["id"] = bid.house.id
        house_dict["address"] = bid.house.full_street_addr
        house_dict["contract_type"] = bid.house.contract_type
        house_dict["contract_detail"] = contract_detail
        house_dict["options"] = options
        house_dict["images"] = images_list
        result.append(house_dict)
    return result


def get_agent_notice_list(decoded_token, pagination):
    email = decoded_token["email"]
    agent = Agent.objects.filter(email=email).first()
    if not agent:
        raise exceptions.AgentDoesNotExist
    notice_list = Notice.objects.filter(type__in=[0, 1]).order_by("created_dt")
    notice_list = Paginator(notice_list, pagination.info_num).page(pagination.page_num).object_list
    return notice_list
