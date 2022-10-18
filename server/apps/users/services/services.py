from http import client

from django.core.exceptions import ObjectDoesNotExist

from ..domains.models import Seller
from ..exceptions import SellerAlreadyExist, SellerDoesNotExist
from ..utils import ClientToken


def issue_access_token(id, client_secret):
    try:
        Seller.objects.get(id=id, client_secret=client_secret)
    except ObjectDoesNotExist:
        raise SellerDoesNotExist
    token = ClientToken(id=id, client_secret=client_secret).encode()
    return {"access": token}


def verify_access_token(token):
    result = ClientToken.decode(token)
    if result:
        return {"token_state": "Y"}
    return {"token_state": "N"}


def create_server_id_for_user(client_secret):
    seller = Seller.client_secret_get_or_none(client_secret)
    if seller:
        raise SellerAlreadyExist
    seller = Seller.objects.create(client_secret=client_secret)
    return seller
