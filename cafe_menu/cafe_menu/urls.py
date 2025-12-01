"""cafe_menu URL Configuration."""
from __future__ import annotations

from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("i18n/", include("django.conf.urls.i18n")),
]

localized_patterns = [
    path("admin/", admin.site.urls),
    path("", include("menu.urls", namespace="menu")),
]

urlpatterns += i18n_patterns(*localized_patterns)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
