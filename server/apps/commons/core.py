from ninja.security import HttpBearer

from apps.users.utils import AgentToken, ClientToken


class AuthBearer(HttpBearer):
    def authenticate(self, request, token):
        result = ClientToken.decode(token)
        return result


class AgentAuthBearer(HttpBearer):
    def authenticate(self, request, token):
        result = AgentToken.decode(token)
        return result
