from django.urls import include, path

from .views import AddressSaveView

urlpatterns = [
    path("address", AddressSaveView.as_view(), name="save_house_address"),
]
