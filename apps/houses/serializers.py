from rest_framework import serializers

from apps.users.models import Seller

from .models import House, HouseBidInfo, HouseImage, HouseOption


class HouseListSerializer(serializers.ModelSerializer):
    """집 정보 기본 시리얼라이저"""

    class Meta:
        model = House
        fields = "__all__"


class AddressSaveSerializer(serializers.ModelSerializer):
    full_addr = serializers.CharField(max_length=256)

    class Meta:
        model = Seller
        fields = ["id", "full_addr"]
        read_only_fields = ["id"]

    def create(self, validated_data):
        request = self.context.get("request")
        seller_id = request.headers.get("seller-id")
        seller = Seller.objects.get(id=seller_id)
        house = House.objects.create(seller=seller, **validated_data)
        return house


class ContractTypeSaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = House
        fields = ["id", "contract_type"]


class HousePriceSaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = House
        fields = ["id", "sell_price", "charter_rent_price", "monthly_rent_price", "deposit_rent_price"]
