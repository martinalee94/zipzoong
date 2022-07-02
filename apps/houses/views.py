from django.db.models import Q
from rest_framework import generics

from .models import House
from .serializers import AddressSaveSerializer, ContractTypeSaveSerializer, HousePriceSaveSerializer


class AddressSaveView(generics.CreateAPIView):
    serializer_class = AddressSaveSerializer


class ContractTypeSaveView(generics.UpdateAPIView):
    queryset = House.objects.all()
    serializer_class = ContractTypeSaveSerializer
    lookup_field = "id"

    def get_queryset(self):
        queryset = House.objects.filter(id=self.kwargs["id"])
        return queryset


class HousePriceSaveView(generics.UpdateAPIView):
    serializer_class = HousePriceSaveSerializer
    lookup_field = "id"

    def get_queryset(self):
        queryset = House.objects.filter(id=self.kwargs["id"])
        return queryset
