from django.core.exceptions import ObjectDoesNotExist

from apps.users.models import Seller

from .exceptions import HouseNotFound, SellerNotFound
from .models import House, HouseDetail, HouseOptionCode
from .utils import OPTION_CODE


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
    try:
        house = House.objects.get(id=house_id)
        house.monthly_deposit = deposit
        house.monthly_rent = monthly_rent
        house.save()
    except ObjectDoesNotExist:
        raise HouseNotFound
    return


def update_house_charter_price(house_id: str, charter_rent: int):
    try:
        house = House.objects.get(id=house_id)
        house.charter_rent = charter_rent
        house.save()
    except ObjectDoesNotExist:
        raise HouseNotFound
    return


def update_house_sale_price(house_id: str, sale_price: int):
    try:
        house = House.objects.get(id=house_id)
        house.sale_price = sale_price
        house.save()
    except ObjectDoesNotExist:
        raise HouseNotFound
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
    try:
        house = House.objects.get(id=house_id)
    except ObjectDoesNotExist:
        raise HouseNotFound

    house_detail = HouseDetail.objects.get_or_create(house=house)[0]
    house_detail.type_option = type
    house_detail.floor_option = floor
    house_detail.rooms_option = room
    house_detail.restroom_option = restroom
    house_detail.duplex_option = duplex
    house_detail.save()
    return house_detail
