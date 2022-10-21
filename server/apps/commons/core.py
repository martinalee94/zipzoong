from ninja.security import HttpBearer

from apps.users.utils import BrokerToken, ClientToken


class AuthBearer(HttpBearer):
    def authenticate(self, request, token):
        result = ClientToken.decode(token)
        return result


class BrokerAuthBearer(HttpBearer):
    def authenticate(self, request, token):
        result = BrokerToken.decode(token)
        return result
