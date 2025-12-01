"""Admin customizations for the cafe menu."""
from __future__ import annotations

from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import MenuCategory, MenuItem, SiteSetting


class MenuItemInline(admin.TabularInline):
    model = MenuItem
    extra = 1
    fields = (
        "name_en",
        "name_fa",
        "price",
        "currency",
        "is_signature",
        "is_available",
    )
    show_change_link = True
    classes = ("collapse",)


@admin.register(MenuCategory)
class MenuCategoryAdmin(admin.ModelAdmin):
    list_display = ("title_en", "title_fa", "display_order", "is_active")
    list_editable = ("display_order", "is_active")
    search_fields = ("title_en", "title_fa")
    list_filter = ("is_active",)
    ordering = ("display_order",)
    inlines = (MenuItemInline,)
    fieldsets = (
        (
            _("Content"),
            {
                "fields": (
                    "title_en",
                    "title_fa",
                    "description_en",
                    "description_fa",
                    "cover_image",
                )
            },
        ),
        (
            _("Display"),
            {"fields": ("display_order", "is_active")},
        ),
    )


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = (
        "name_en",
        "category",
        "price",
        "currency",
        "is_signature",
        "is_available",
        "rating",
        "updated_at",
    )
    list_filter = ("category", "currency", "is_signature", "is_available")
    search_fields = ("name_en", "name_fa", "description_en", "description_fa")
    autocomplete_fields = ("category",)
    readonly_fields = ("created_at", "updated_at")
    prepopulated_fields = {"slug": ("name_en",)}
    fieldsets = (
        (
            _("Basics"),
            {
                "fields": (
                    "category",
                    "name_en",
                    "name_fa",
                    "slug",
                    "description_en",
                    "description_fa",
                )
            },
        ),
        (
            _("Pricing & Availability"),
            {
                "fields": (
                    "price",
                    "currency",
                    "is_signature",
                    "is_available",
                    "rating",
                )
            },
        ),
        (
            _("Metadata"),
            {
                "fields": (
                    "calories",
                    "preparation_time",
                    "highlight_badge_en",
                    "highlight_badge_fa",
                    "image",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            _("Timestamps"),
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )


@admin.register(SiteSetting)
class SiteSettingAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            _("Identity"),
            {"fields": ("site_name_en", "site_name_fa", "site_logo", "site_favicon")},
        ),
        (
            _("Hero Section"),
            {"fields": ("hero_headline_en", "hero_headline_fa", "hero_subtitle_en", "hero_subtitle_fa")},
        ),
        (
            _("Contact"),
            {"fields": ("contact_email", "contact_phone", "contact_whatsapp", "address_en", "address_fa", "opening_hours")},
        ),
        (
            _("Footer"),
            {"fields": ("footer_text_en", "footer_text_fa", "footer_links", "social_links")},
        ),
        (
            _("SEO"),
            {"fields": ("seo_description_en", "seo_description_fa")},
        ),
    )
    list_display = ("site_name", "contact_email", "opening_hours")

    def has_add_permission(self, request):
        if SiteSetting.objects.exists():
            return False
        return super().has_add_permission(request)

