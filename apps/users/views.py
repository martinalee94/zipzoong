from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.permissions import AllowAny

from apps.users.models import Seller

from .serializers import SellerHouseInfoSerializer, SellerRegisterSerializer


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


class SellerHouseInfoView(generics.ListAPIView):
    queryset = Seller.objects.all()
    serializer_class = SellerHouseInfoSerializer
    permission_classes = [AllowAny]

    def filter_queryset(self, queryset):
        queryset = Seller.objects.prefetch_related("house").filter(
            id=self.request.headers.get("seller-id")
        )
        return queryset
