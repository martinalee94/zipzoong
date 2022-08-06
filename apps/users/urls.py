from django import views
from django.urls import include, path

from .views import SellerRegisterView

urlpatterns = [
    path("sellers/register", SellerRegisterView.as_view(), name="seller_register"),
]
