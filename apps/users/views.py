from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics

from .serializers import SellerRegisterSerializer


class SellerRegisterView(generics.CreateAPIView):
    serializer_class = SellerRegisterSerializer

    @swagger_auto_schema(
        operation_summary="판매자 가입 API",
        responses={
            201: "가입 성공",
            400: "상세 에러 메세지 확인",
        },
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
