from apps.users.utils import BrokerToken

from ..domains.models import Broker
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
