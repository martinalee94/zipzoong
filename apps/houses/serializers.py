from django.db import transaction
from rest_framework import serializers

from apps.users.models import Seller
from apps.users.utils import get_seller_from_header

from .models import House


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
