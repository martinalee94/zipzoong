from django.contrib import admin
from django.urls import include, path

extrapatterns = [
    path("houses/", include("apps.houses.urls")),
    path("sellers/", include("apps.sellers.urls")),
]
urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(extrapatterns)),
]
