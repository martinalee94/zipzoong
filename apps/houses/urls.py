from django.urls import path

from .views import (
    GetHouseInfoView,
    UploadAddressView,
    UploadCharterPriceView,
    UploadContractTypeView,
    UploadHouseImageView,
    UploadHouseOptionView,
    UploadMonthlyPriceView,
    UploadSellPriceView,
)

urlpatterns = [
    path("<int:id>", GetHouseInfoView.as_view(), name="get_house_info"),
    path("address", UploadAddressView.as_view(), name="save_house_address"),
    path(
        "contract-type/<int:id>", UploadContractTypeView.as_view(), name="save_house_contract_type"
    ),
    path("monthly-price/<int:id>", UploadMonthlyPriceView.as_view(), name="save_monthly_price"),
    path("charter-price/<int:id>", UploadCharterPriceView.as_view(), name="save_charter_price"),
    path("sell-price/<int:id>", UploadSellPriceView.as_view(), name="save_sell_price"),
    path("options/<int:id>", UploadHouseOptionView.as_view(), name="save_house_option"),
    path("images/<int:id>", UploadHouseImageView.as_view(), name="save_house_images"),
]
