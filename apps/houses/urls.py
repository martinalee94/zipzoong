from django.urls import include, path

from .views import AddressSaveView, ContractTypeSaveView, HousePriceSaveView, GetOneHouseInfoView

urlpatterns = [
    path("<int:id>", GetOneHouseInfoView.as_view(), name="get_one_house_info"),
    path("address", AddressSaveView.as_view(), name="save_house_address"),
    path("<int:id>/contract", ContractTypeSaveView.as_view(), name="save_house_contract_type"),
    path("<int:id>/price", HousePriceSaveView.as_view(), name="save_house_price"),
]
