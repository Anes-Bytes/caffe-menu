"""URL patterns for the menu app."""
from __future__ import annotations

from django.urls import path

from .views import HomePageView

app_name = "menu"

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
]

