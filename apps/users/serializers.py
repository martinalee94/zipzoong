from rest_framework import serializers

from apps.houses.serializers import HouseListSerializer

from .models import Agent, Seller


class SellerRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seller
        fields = ["id", "device"]
        read_only_fields = ["id"]


class SellerHouseInfoSerializer(serializers.ModelSerializer):
    house = HouseListSerializer(many=True)

    class Meta:
        model = Seller
        fields = ["id", "device", "house"]
        read_only_fields = ["house"]
