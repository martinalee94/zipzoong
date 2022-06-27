from django.contrib import admin
from django.urls import path, include

from .views import HelloView
urlpatterns = [
    path('hi/', HelloView, name="hi_view"),
]
