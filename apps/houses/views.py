from rest_framework import generics

from .serializers import AddressSaveSerializer


class AddressSaveView(generics.CreateAPIView):
    serializer_class = AddressSaveSerializer
