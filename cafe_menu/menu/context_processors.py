"""Context processors for the menu app."""
from __future__ import annotations

from django.conf import settings
from django.core.cache import cache

from .models import SITE_SETTINGS_CACHE_KEY, SiteSetting


def _language_paths(request):
    """Build localized URLs for the current path."""

    path = request.path_info or "/"
    trimmed = path.lstrip("/")
    parts = trimmed.split("/", 1) if trimmed else []
    language_codes = {code for code, _ in settings.LANGUAGES}

    if parts and parts[0] in language_codes:
        remainder = parts[1] if len(parts) > 1 else ""
    else:
        remainder = trimmed

    remainder = remainder.strip("/")

    urls = {}
    for code, _ in settings.LANGUAGES:
        suffix = f"{remainder}/" if remainder else ""
        urls[code] = f"/{code}/" + suffix
    return urls


def global_settings(request):
    """Expose the singleton site settings instance to every template."""

    settings_instance = cache.get(SITE_SETTINGS_CACHE_KEY)
    if settings_instance is None:
        settings_instance = SiteSetting.objects.first()
        if settings_instance is None:
            # Provide a lightweight placeholder to keep templates from breaking.
            settings_instance = SiteSetting(site_name_en="Cafe Menu")
        cache.set(SITE_SETTINGS_CACHE_KEY, settings_instance, 60 * 5)

    language_urls = _language_paths(request)

    return {
        "site_settings": settings_instance,
        "language_urls": language_urls,
    }

