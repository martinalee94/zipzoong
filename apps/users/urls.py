from django.urls import path


from .views import SellerRegisterView

urlpatterns = [
    path("sellers/register", SellerRegisterView.as_view(), name="seller_register"),
]
