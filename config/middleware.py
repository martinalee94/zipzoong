import re

from apps.users.models import Seller
from apps.users.utils import decode_user_token
from django.http import HttpResponse, JsonResponse
from django.utils.deprecation import MiddlewareMixin
from rest_framework import status


class CustomSellerCheckMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response
        self.API_URLS = [
            re.compile(r"^(.*)/api"),
            re.compile(r"^api"),
        ]

    def process_request(self, request):
        if request.path.startswith("/api/users/sellers/register"):
            return None
        if not request.headers.get("Authorization"):
            return JsonResponse(
                data={
                    "status": status.HTTP_401_UNAUTHORIZED,
                    "message": "서비스 이용을 위해서는 토큰이 필요합니다.",
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )

        try:
            token = request.headers.get("Authorization").split()[1]
            decode_user_token(token)
        except Exception:
            return JsonResponse(
                data={
                    "status": status.HTTP_401_UNAUTHORIZED,
                    "message": "유효한 토큰을 전송하세요.",
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )
