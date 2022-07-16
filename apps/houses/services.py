from apps.users.utils import get_seller_from_header

from .models import House


def check_seller_own_house(seller_info, house_id):
    house = House.objects.get(id=house_id)
    if house.seller.id == seller_info["user_id"]:
        return True
    return False
