from http import client

from apps.brokers.domains.models import Broker
from django.core.exceptions import ObjectDoesNotExist

from ..domains.models import Seller
from ..exceptions import BrokerDoesNotExist, SellerAlreadyExist, SellerDoesNotExist
from ..utils import BrokerToken, ClientToken


def issue_seller_access_token(id, client_secret):
    try:
        Seller.objects.get(id=id, client_secret=client_secret)
    except ObjectDoesNotExist:
        raise SellerDoesNotExist
    token = ClientToken(id=id, client_secret=client_secret).encode()
    return {"access": token}


def verify_seller_access_token(token):
    result = ClientToken.decode(token)
    if result:
        return {"token_state": "Y"}
    return {"token_state": "N"}


def issue_broker_access_token(email, password):
    try:
        Broker.objects.get(email=email)
    except ObjectDoesNotExist:
        raise BrokerDoesNotExist
    token = BrokerToken(email=email, password=password).encode()
    return {"access": token}


def verify_broker_access_token(token):
    result = BrokerToken.decode(token)
    if result:
        return {"token_state": "Y"}
    return {"token_state": "N"}


def create_server_id_for_user(client_secret):
    seller = Seller.client_secret_get_or_none(client_secret)
    if seller:
        raise SellerAlreadyExist
    seller = Seller.objects.create(client_secret=client_secret)
    return seller
