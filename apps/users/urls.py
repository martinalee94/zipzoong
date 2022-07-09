from django import views
from django.urls import include, path

from .views import SellerHouseInfoView, SellerRegisterView

urlpatterns = [
    path("sellers/register", SellerRegisterView.as_view(), name="seller_register"),
    path("sellers/house-info", SellerHouseInfoView.as_view(), name="seller_house_info"),
]
