from datetime import datetime
from pathlib import Path
from random import randrange

from apps.commons.exceptions import ImageSizeIsExceeded, ImageTypeIsNotAllowed
from apps.users.domains.models import Seller
from asgiref.sync import sync_to_async
from config.settings.base import MEDIA_ROOT
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from PIL import Image

from ..apis import schemas
from ..domains.models import House, HouseDetail, HouseImage, HouseOptionCode
from ..exceptions import HouseNotFound, SellerNotFound
from .enums import ContractTypes
from .utils import ALLOWED_IMAGE_SIZE, ALLOWED_IMAGE_TYPE, OPTION_CODE


def _check_house_exist(house_id):
    try:
        house = House.objects.get(id=house_id)
    except ObjectDoesNotExist:
        raise HouseNotFound
    return house


def add_house(house_id: str, seller_id: str, addr_info: schemas.CreateHouseAddressInSchema):
    seller = Seller.objects.filter(id=seller_id)
    if not seller:
        raise SellerNotFound

    addr_info = addr_info.dict()
    try:
        House.objects.filter(id=house_id).update(**addr_info)
        house = House.objects.get(id=house_id)
    except Exception as e:
        house = House.create_house(seller=seller[0], **addr_info)
        HouseDetail.objects.create(house=house)
    return house


def get_default_house_contract_type_list():
    result = {}
    contract_types = HouseOptionCode.objects.filter(type=1001)
    for contract_type in contract_types:
        result[contract_type.key] = contract_type.value
    return result


def update_house_monthly_price(house_id: str, deposit: int, monthly_rent: int):
    house = _check_house_exist(house_id)
    house.monthly_deposit = deposit
    house.monthly_rent = monthly_rent
    house.contract_type = ContractTypes.MONTHLY_RENT
    house.save()
    return


def update_house_charter_price(house_id: str, charter_rent: int):
    house = _check_house_exist(house_id)
    house.charter_rent = charter_rent
    house.contract_type = ContractTypes.CHARTERED_RENT
    house.save()
    return


def update_house_sale_price(house_id: str, sale_price: int):
    house = _check_house_exist(house_id)
    house.sale_price = sale_price
    house.contract_type = ContractTypes.SALE
    house.save()
    return


def get_default_house_options_list():
    result = {}
    option_codes = HouseOptionCode.objects.filter(type__gte=2000, type__lt=3000)
    for code in option_codes:
        if result.get(code.type):
            result[code.type][code.key] = code.value
        else:
            result[code.type] = {code.key: code.value}
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
def add_house_images(house_id: str, image, num: int):
    house = _check_house_exist(house_id)

    if image.size > ALLOWED_IMAGE_SIZE:
        raise ImageSizeIsExceeded
    origin_image_type = image.name.split(".")[-1].lower()
    if origin_image_type not in ALLOWED_IMAGE_TYPE:
        raise ImageTypeIsNotAllowed

    file_date_key = datetime.now().strftime("%Y%m%d_%H%M%S")

    origin_image = Image.open(image)
    origin_width, origin_height = origin_image.size

    Path(MEDIA_ROOT + f"/{house_id}").mkdir(parents=True, exist_ok=True)
    path = MEDIA_ROOT + f"/{house_id}/{file_date_key}_{num}.png"
    origin_image.save(path, "PNG")

    image = HouseImage(
        house=house,
        path=path,
        name=f"{file_date_key}_{num}.png",
        type="png",
        size=image.size,
        width=origin_width,
        height=origin_height,
        wh_type=1,
    )
    image.save()
    return


def get_house_info_list(decoded_token, pagination: schemas.PaginationListSchema):
    result = []
    seller_id = decoded_token["id"]
    houses = House.objects.filter(seller_id=seller_id).prefetch_related("detail")
    houses.order_by("created_dt")
    houses = Paginator(houses, pagination.info_num).page(pagination.page_num).object_list

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
