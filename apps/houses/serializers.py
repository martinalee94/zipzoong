from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.forms import ValidationError
from rest_framework import serializers, status

from apps.users.models import Seller
from apps.users.utils import get_seller_from_header

from .models import House, HouseImage, HouseOption


class HouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = House
        fields = "__all__"


class HouseOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = HouseOption
        exclude = ["id", "created_at", "modified_at", "house"]


class HouseImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = HouseImage
        exclude = ["created_at", "modified_at", "house"]


class GetHouseInfoSerializer(serializers.ModelSerializer):
    options = HouseOptionSerializer(read_only=True)
    images = HouseImageSerializer(read_only=True, many=True)

    class Meta:
        model = House
        fields = "__all__"


class UploadAddressSerializer(serializers.ModelSerializer):
    full_addr = serializers.CharField(max_length=256)

    class Meta:
        model = Seller
        fields = ["id", "full_addr"]
        read_only_fields = ["id"]

    @transaction.atomic
    def create(self, validated_data):
        request = self.context.get("request")
        seller_info = get_seller_from_header(request)
        seller = Seller.objects.get(device=seller_info["device"])
        house = House.objects.create(seller=seller, **validated_data)
        return house


class UploadContractTypeSerializer(serializers.ModelSerializer):
    type = serializers.CharField(write_only=True, source="contract_type")

    class Meta:
        model = House
        fields = ["type"]


class UploadMonthlyPriceSerializer(serializers.ModelSerializer):
    deposit = serializers.IntegerField(write_only=True, source="deposit_rent_price")
    monthly_price = serializers.IntegerField(write_only=True, source="monthly_rent_price")

    class Meta:
        model = House
        fields = ["deposit", "monthly_price"]


class UploadCharterPriceSerializer(serializers.ModelSerializer):
    charter_price = serializers.IntegerField(write_only=True, source="charter_rent_price")

    class Meta:
        model = House
        fields = ["charter_price"]


class UploadSellPriceSerializer(serializers.ModelSerializer):
    sell_price = serializers.IntegerField(write_only=True, source="sell_price")

    class Meta:
        model = House
        fields = ["sell_price"]


class UploadHouseOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = HouseOption
        exclude = ["created_at", "modified_at", "house"]


class UploadHouseImageSerializer(serializers.ModelSerializer):
    file = serializers.ImageField(write_only=True, source="path")

    class Meta:
        model = HouseImage
        fields = ["file"]

    @transaction.atomic
    def create(self, validated_data, *args, **kwargs):
        request = self.context.get("request")
        size = request.FILES["file"].size
        type = request.FILES["file"].name.split(".")[-1]
        house_id = request.path.split("/")[-1]
        house = House.objects.get(id=house_id)
        image = HouseImage.objects.create(house=house, type=type, size=size, **validated_data)
        return image
