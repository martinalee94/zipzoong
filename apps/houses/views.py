from rest_framework import generics

from .serializers import UploadAddressSerializer


class UploadAddressView(generics.CreateAPIView):
    serializer_class = UploadAddressSerializer
