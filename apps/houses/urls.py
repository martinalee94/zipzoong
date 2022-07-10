from django.urls import path

from .views import UploadAddressView

urlpatterns = [
    path("address", UploadAddressView.as_view(), name="save_house_address"),
]
