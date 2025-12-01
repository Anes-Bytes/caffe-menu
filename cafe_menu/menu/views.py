"""Public views for the cafe menu."""
from __future__ import annotations

from itertools import islice

from django.conf import settings
from django.db.models import Prefetch
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from django.views.generic import TemplateView

from .models import MenuCategory, MenuItem


@method_decorator(cache_page(60 * 5), name="dispatch")
@method_decorator(vary_on_cookie, name="dispatch")
class HomePageView(TemplateView):
    template_name = "menu/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = list(
            MenuCategory.objects.filter(is_active=True)
            .prefetch_related(
                Prefetch(
                    "items",
                    queryset=MenuItem.objects.filter(is_available=True).order_by("-is_signature", "name_en"),
                )
            )
            .order_by("display_order")
        )
        context["categories"] = categories
        context["signature_items"] = list(
            islice(
                (
                    item
                    for category in categories
                    for item in category.items.all()
                    if item.is_signature
                ),
                4,
            )
        )
        language_cookie = self.request.COOKIES.get(settings.LANGUAGE_COOKIE_NAME)
        current_language = getattr(self.request, "LANGUAGE_CODE", None)
        default_lang = settings.LANGUAGE_CODE.split("-")[0]
        context["language_selected"] = bool(
            language_cookie
            or (current_language and current_language.split("-")[0] != default_lang)
        )
        return context

