from django.db.models import Q
from rest_framework import generics

from .models import House, HouseOption
from .serializers import AddressSaveSerializer, ContractTypeSaveSerializer, HousePriceSaveSerializer, GetOneHouseInfoSerializer


class GetOneHouseInfoView(generics.RetrieveAPIView):
    serializer_class = GetOneHouseInfoSerializer
    lookup_field = "id"

    def get_queryset(self):
        queryset = House.objects.filter(id=self.kwargs["id"]).prefetch_related("options", "images")
        return queryset


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
