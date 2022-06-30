from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Zipzoong API",
        default_version="0.1",
        description="Zipzoong API Docs",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

extrapatterns = [
    path(
        "docs/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("houses/", include("apps.houses.urls")),
    path("users/", include("apps.users.urls")),
]
urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(extrapatterns)),
]
