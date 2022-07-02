from django import views
from django.urls import include, path

from .views import SellerExistSaveView

urlpatterns = [
    path(
        "sellers/",
        SellerExistSaveView.as_view(),
        name="seller_exists_or_save",
    ),
]
