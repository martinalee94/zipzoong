from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from apps.users.models import Seller

from .serializers import SellerGetSaveSerializer


class SellerExistSaveView(generics.CreateAPIView):
    serializer_class = SellerGetSaveSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except Exception:
            seller = Seller.objects.get(id=request.data["id"])
            serializer = self.get_serializer(seller)
            return Response(serializer.data)
