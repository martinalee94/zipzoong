from rest_framework import serializers

from apps.houses.models import House
from apps.houses.serializers import HouseListSerializer

from .models import Agent, Seller


class SellerGetSaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seller
        fields = ["id", "uniq_num"]
        read_only_fields = ["uniq_num"]


class SellerHouseInfoSerializer(serializers.ModelSerializer):
    house = HouseListSerializer(many=True)

    class Meta:
        model = Seller
        fields = ["id", "uniq_num", "house"]
        read_only_fields = ["house"]
