from rest_framework import serializers

from .models import Seller
from .utils import create_user_token


class SellerRegisterSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    device = serializers.CharField()
    token = serializers.SerializerMethodField()

    def create(self, validated_data):
        device = validated_data.get("device")
        seller = Seller.objects.get_or_create(device=device)[0]
        return seller

    def get_token(self, obj):
        token = create_user_token(obj.id, obj.device)
        return token

    class Meta:
        fields = ["id", "device", "token"]
        read_only_fields = ["id", "token"]
