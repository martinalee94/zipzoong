from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, JsonResponse
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from apps.users.utils import get_seller_from_header

from .models import House
from .serializers import (
    UploadAddressSerializer,
    UploadCharterPriceSerializer,
    UploadContractTypeSerializer,
    UploadMonthlyPriceSerializer,
    UploadSellPriceSerializer,
)
from .services import check_seller_own_house


class UploadAddressView(generics.CreateAPIView):
    serializer_class = UploadAddressSerializer
    # permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="매물 등록(집주소) API",
        responses={
            201: "등록 성공",
        },
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class UploadContractTypeView(generics.UpdateAPIView):
    serializer_class = UploadContractTypeSerializer
    queryset = House.objects.all()
    lookup_field = "id"
    permission_classes = [IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(
        operation_summary="매물 계약형태 등록 API",
        responses={200: "등록 성공", 400: "오류 메세지 확인"},
    )
    def patch(self, request, *args, **kwargs):
        seller_info = get_seller_from_header(request)
        try:
            if check_seller_own_house(seller_info, self.kwargs["id"]):
                return self.partial_update(request, *args, **kwargs)
        except ObjectDoesNotExist:
            return JsonResponse(data="올바른 매물 ID를 입력해 주세요", status=status.HTTP_400_BAD_REQUEST)
        else:
            return JsonResponse(data="소유한 매물이 아닙니다", status=status.HTTP_400_BAD_REQUEST)


class UploadMonthlyPriceView(generics.UpdateAPIView):
    serializer_class = UploadMonthlyPriceSerializer
    queryset = House.objects.all()
    lookup_field = "id"

    @swagger_auto_schema(
        operation_summary="월세 금액 입력 API",
        responses={200: "등록 성공", 400: "오류 메세지 확인"},
    )
    def patch(self, request, *args, **kwargs):
        seller_info = get_seller_from_header(request)
        try:
            if check_seller_own_house(seller_info, self.kwargs["id"]):
                return self.partial_update(request, *args, **kwargs)
        except ObjectDoesNotExist:
            return Response(data="올바른 매물 ID를 입력해 주세요", status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data="소유한 매물이 아닙니다", status=status.HTTP_400_BAD_REQUEST)


class UploadCharterPriceView(generics.UpdateAPIView):
    serializer_class = UploadCharterPriceSerializer
    queryset = House.objects.all()
    lookup_field = "id"

    @swagger_auto_schema(
        operation_summary="전세 금액 입력 API",
        responses={200: "등록 성공", 400: "오류 메세지 확인"},
    )
    def patch(self, request, *args, **kwargs):
        seller_info = get_seller_from_header(request)
        try:
            if check_seller_own_house(seller_info, self.kwargs["id"]):
                return self.partial_update(request, *args, **kwargs)
        except ObjectDoesNotExist:
            return Response(data="올바른 매물 ID를 입력해 주세요", status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data="소유한 매물이 아닙니다", status=status.HTTP_400_BAD_REQUEST)


class UploadSellPriceView(generics.UpdateAPIView):
    serializer_class = UploadSellPriceSerializer
    queryset = House.objects.all()
    lookup_field = "id"

    @swagger_auto_schema(
        operation_summary="매매 금액 입력 API",
        responses={200: "등록 성공", 400: "오류 메세지 확인"},
    )
    def patch(self, request, *args, **kwargs):
        seller_info = get_seller_from_header(request)
        try:
            if check_seller_own_house(seller_info, self.kwargs["id"]):
                return self.partial_update(request, *args, **kwargs)
        except ObjectDoesNotExist:
            return Response(data="올바른 매물 ID를 입력해 주세요", status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data="소유한 매물이 아닙니다", status=status.HTTP_400_BAD_REQUEST)
