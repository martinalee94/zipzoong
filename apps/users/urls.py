from django import views
from django.urls import include, path

from .views import SellerExistSaveView, SellerHouseInfoView

urlpatterns = [
    path(
        "sellers/",
        SellerExistSaveView.as_view(),
        name="seller_exists_or_save",
    ),
    path("sellers/house-info", SellerHouseInfoView.as_view(), name="seller_house_info"),
]
