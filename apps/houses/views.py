from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics

from .serializers import UploadAddressSerializer


class UploadAddressView(generics.CreateAPIView):
    serializer_class = UploadAddressSerializer

    @swagger_auto_schema(
        operation_summary="매물 등록(집주소) API",
        responses={
            201: "등록 성공",
        },
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)