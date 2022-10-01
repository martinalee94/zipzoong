from ninja.security import HttpBearer

from apps.users.utils import ClientToken


class AuthBearer(HttpBearer):
    def authenticate(self, request, token):
        result = ClientToken.decode(token)
        return result
