import os
from datetime import datetime
from pathlib import Path
from random import randrange

from asgiref.sync import sync_to_async
from config.settings.base import MEDIA_ROOT
from django.core.exceptions import ObjectDoesNotExist
from PIL import Image

from apps.users.models import Seller

from .exceptions import HouseNotFound, ImageSizeIsExceeded, ImageTypeIsNotAllowed, SellerNotFound
from .models import House, HouseDetail, HouseImage, HouseOptionCode
from .utils import ALLOWED_IMAGE_SIZE, ALLOWED_IMAGE_TYPE, OPTION_CODE


def _check_house_exist(house_id):
    try:
        house = House.objects.get(id=house_id)
    except ObjectDoesNotExist:
        raise HouseNotFound
    return house


def add_house(
    seller_id: str,
    sido_addr: str,
    gungu_addr: str,
    street_addr: str,
    detail_addr: str = None,
    postal_code: str = None,
):
    seller = Seller.objects.filter(id=seller_id)
    if not seller:
        raise SellerNotFound

    house = House.create_house(
        sido_addr=sido_addr,
        gungu_addr=gungu_addr,
        street_addr=street_addr,
        detail_addr=detail_addr,
        postal_code=postal_code,
    )
    return house


def update_house_monthly_price(house_id: str, deposit: int, monthly_rent: int):
    house = _check_house_exist(house_id)
    house.monthly_deposit = deposit
    house.monthly_rent = monthly_rent
    house.save()
    return


def update_house_charter_price(house_id: str, charter_rent: int):
    house = _check_house_exist(house_id)
    house.charter_rent = charter_rent
    house.save()
    return


def update_house_sale_price(house_id: str, sale_price: int):
    house = _check_house_exist(house_id)
    house.sale_price = sale_price
    house.save()
    return


def get_default_house_options_list():
    option_codes = HouseOptionCode.objects.all()
    result = {}
    for code in option_codes:
        option_type = OPTION_CODE[code.type]
        if not result.get(option_type):
            result[option_type] = [code.value]
        else:
            result[option_type].append(code.value)
    return result


def update_house_options(
    house_id: str,
    type: str = None,
    floor: str = None,
    room: str = None,
    restroom: str = None,
    duplex: str = None,
):
    house = _check_house_exist(house_id)

    house_detail = HouseDetail.objects.get_or_create(house=house)[0]
    house_detail.type_option = type
    house_detail.floor_option = floor
    house_detail.rooms_option = room
    house_detail.restroom_option = restroom
    house_detail.duplex_option = duplex
    house_detail.save()
    return house_detail


@sync_to_async
def add_house_images(house_id, image, file_date_key):
    house = _check_house_exist(house_id)

    if image.size > ALLOWED_IMAGE_SIZE:
        raise ImageSizeIsExceeded
    origin_image_type = image.name.split(".")[-1].lower()
    if origin_image_type not in ALLOWED_IMAGE_TYPE:
        raise ImageTypeIsNotAllowed

    # 파일이름 "houseid_filedatekey_filenamekey"
    file_name_key = randrange(10000000, 99999999)

    origin_image = Image.open(image)
    origin_width, origin_height = origin_image.size

    Path(MEDIA_ROOT + f"/{house_id}/{file_date_key}").mkdir(parents=True, exist_ok=True)
    path = (
        MEDIA_ROOT + f"/{house_id}/{file_date_key}/{house_id}_{file_date_key}_{file_name_key}.png"
    )
    origin_image.save(path, "PNG")

    image = HouseImage(
        house=house,
        path=f"/{house_id}/{file_date_key}/{house_id}_{file_date_key}_{file_name_key}.png",
        name=f"{house_id}_{file_date_key}_{file_name_key}.png",
        type="png",
        size=image.size,
        width=origin_width,
        height=origin_height,
        wh_type=1,
    )
    image.save()
    return


# @sync_to_async
# def add_house_images(house_id, images):
#     house = _check_house_exist(house_id)

#     for image in images:
#         if image.size > ALLOWED_IMAGE_SIZE:
#             raise ImageSizeIsExceeded
#         origin_image_type = image.name.split(".")[-1].lower()
#         if origin_image_type not in ALLOWED_IMAGE_TYPE:
#             raise ImageTypeIsNotAllowed

#     # 파일이름 "houseid_filedatekey_filenamekey"
#     file_date_key = datetime.now().strftime("%Y%m%d%H%M%S")
#     for image in images:
#         file_name_key = randrange(10000000, 99999999)

#         origin_image = Image.open(image)
#         origin_width, origin_height = origin_image.size

#         Path(MEDIA_ROOT + f"/{house_id}/{file_date_key}").mkdir(parents=True, exist_ok=True)
#         path = (
#             MEDIA_ROOT
#             + f"/{house_id}/{file_date_key}/{house_id}_{file_date_key}_{file_name_key}.png"
#         )
#         origin_image.save(path, "PNG")

#         image = HouseImage(
#             house=house,
#             path=path,
#             name=f"{house_id}_{file_date_key}_{file_name_key}.png",
#             type="png",
#             size=image.size,
#             width=origin_width,
#             height=origin_height,
#             wh_type=1,
#         )
#         image.save()

#     return


def get_house_images(house_id):
    return
