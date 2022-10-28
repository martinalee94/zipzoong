from http import client

from apps.agents.domains.models import Agent
from django.core.exceptions import ObjectDoesNotExist

from ..domains.models import Seller
from ..exceptions import AgentDoesNotExist, SellerAlreadyExist, SellerDoesNotExist
from ..utils import AgentToken, ClientToken


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


def issue_agent_access_token(email, password):
    try:
        Agent.objects.get(email=email)
    except ObjectDoesNotExist:
        raise AgentDoesNotExist
    token = AgentToken(email=email, password=password).encode()
    return {"access": token}


def verify_agent_access_token(token):
    result = AgentToken.decode(token)
    if result:
        return {"token_state": "Y"}
    return {"token_state": "N"}


def create_server_id_for_user(client_secret):
    seller = Seller.client_secret_get_or_none(client_secret)
    if seller:
        raise SellerAlreadyExist
    seller = Seller.objects.create(client_secret=client_secret)
    return seller
