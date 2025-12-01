from __future__ import annotations

from decimal import Decimal

from django.core.cache import cache
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone, translation
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _


class TimeStampedModel(models.Model):
    """Abstract model that stores creation and update timestamps."""

    created_at = models.DateTimeField(_("created at"), default=timezone.now, editable=False)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)

    class Meta:
        abstract = True
        ordering = ("-created_at",)


class TranslatableFieldsMixin:
    """Mixin that returns the field value that matches the current language."""

    def translate(self, field_prefix: str) -> str:
        lang = (translation.get_language() or "en").split("-")[0]
        preferred_field = f"{field_prefix}_{lang}"
        fallback_field = f"{field_prefix}_en"
        return getattr(self, preferred_field, None) or getattr(self, fallback_field, "")


SITE_SETTINGS_CACHE_KEY = "menu.site_settings"


class SiteSetting(TranslatableFieldsMixin, models.Model):
    """Singleton model that stores global site configuration."""

    site_name_en = models.CharField(_("site name (EN)"), max_length=120)
    site_name_fa = models.CharField(_("site name (FA)"), max_length=120, blank=True)
    site_logo = models.ImageField(_("logo"), upload_to="branding/", blank=True, null=True)
    site_favicon = models.ImageField(_("favicon"), upload_to="branding/", blank=True, null=True)
    hero_headline_en = models.CharField(_("hero headline (EN)"), max_length=180, blank=True)
    hero_headline_fa = models.CharField(_("hero headline (FA)"), max_length=180, blank=True)
    hero_subtitle_en = models.CharField(_("hero subtitle (EN)"), max_length=220, blank=True)
    hero_subtitle_fa = models.CharField(_("hero subtitle (FA)"), max_length=220, blank=True)
    contact_email = models.EmailField(_("contact email"), blank=True)
    contact_phone = models.CharField(_("contact phone"), max_length=40, blank=True)
    contact_whatsapp = models.CharField(_("whatsapp"), max_length=80, blank=True)
    address_en = models.CharField(_("address (EN)"), max_length=220, blank=True)
    address_fa = models.CharField(_("address (FA)"), max_length=220, blank=True)
    opening_hours = models.CharField(_("opening hours"), max_length=180, default="08:00 - 23:00")
    footer_text_en = models.CharField(_("footer text (EN)"), max_length=200, blank=True)
    footer_text_fa = models.CharField(_("footer text (FA)"), max_length=200, blank=True)
    footer_links = models.JSONField(_("footer links"), default=list, blank=True)
    social_links = models.JSONField(_("social links"), default=dict, blank=True)
    seo_description_en = models.TextField(_("SEO description (EN)"), blank=True)
    seo_description_fa = models.TextField(_("SEO description (FA)"), blank=True)

    class Meta:
        verbose_name = _("site settings")
        verbose_name_plural = _("site settings")

    @property
    def site_name(self) -> str:
        return self.translate("site_name") or self.site_name_en

    def localized_value(self, field_prefix: str, fallback: str = "") -> str:
        return self.translate(field_prefix) or fallback

    @property
    def hero_headline(self) -> str:
        return self.localized_value("hero_headline", self.site_name)

    @property
    def hero_subtitle(self) -> str:
        return self.localized_value("hero_subtitle")

    @property
    def address(self) -> str:
        return self.localized_value("address")

    @property
    def footer_text(self) -> str:
        return self.localized_value("footer_text")

    @property
    def seo_description(self) -> str:
        return self.localized_value("seo_description")

    def __str__(self) -> str:
        return self.site_name

    def save(self, *args, **kwargs) -> None:
        super().save(*args, **kwargs)
        cache.delete(SITE_SETTINGS_CACHE_KEY)

    def delete(self, using=None, keep_parents=False):
        response = super().delete(using=using, keep_parents=keep_parents)
        cache.delete(SITE_SETTINGS_CACHE_KEY)
        return response


class MenuCategory(TimeStampedModel, TranslatableFieldsMixin):
    """Menu sections such as Coffee, Desserts, etc."""

    title_en = models.CharField(_("title (EN)"), max_length=120)
    title_fa = models.CharField(_("title (FA)"), max_length=120)
    description_en = models.TextField(_("description (EN)"), blank=True)
    description_fa = models.TextField(_("description (FA)"), blank=True)
    cover_image = models.ImageField(_("cover image"), upload_to="menu/categories/", blank=True, null=True)
    display_order = models.PositiveIntegerField(_("display order"), default=0)
    is_active = models.BooleanField(_("active"), default=True)

    class Meta(TimeStampedModel.Meta):
        ordering = ("display_order",)
        verbose_name = _("category")
        verbose_name_plural = _("categories")

    @property
    def title(self) -> str:
        return self.translate("title")

    @property
    def description(self) -> str:
        return self.translate("description")

    def __str__(self) -> str:
        return self.title


class MenuItem(TimeStampedModel, TranslatableFieldsMixin):
    """Menu items managed via the admin."""

    CURRENCY_CHOICES = [
        ("IRR", _("Iranian Rial")),
        ("USD", _("US Dollar")),
    ]

    category = models.ForeignKey(MenuCategory, related_name="items", on_delete=models.CASCADE)
    name_en = models.CharField(_("name (EN)"), max_length=140)
    name_fa = models.CharField(_("name (FA)"), max_length=140)
    slug = models.SlugField(_("slug"), unique=True, blank=True)
    description_en = models.TextField(_("description (EN)"), blank=True)
    description_fa = models.TextField(_("description (FA)"), blank=True)
    price = models.DecimalField(
        _("price"),
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00"))],
    )
    currency = models.CharField(_("currency"), max_length=3, choices=CURRENCY_CHOICES, default="IRR")
    image = models.ImageField(_("image"), upload_to="menu/items/", blank=True, null=True)
    is_signature = models.BooleanField(_("signature item"), default=False)
    is_available = models.BooleanField(_("available"), default=True)
    calories = models.PositiveIntegerField(_("calories"), blank=True, null=True)
    preparation_time = models.CharField(_("prep time"), max_length=40, blank=True)
    highlight_badge_en = models.CharField(_("badge (EN)"), max_length=60, blank=True)
    highlight_badge_fa = models.CharField(_("badge (FA)"), max_length=60, blank=True)
    rating = models.DecimalField(
        _("rating"),
        max_digits=2,
        decimal_places=1,
        blank=True,
        null=True,
        validators=[
            MinValueValidator(Decimal("0.0")),
            MaxValueValidator(Decimal("5.0")),
        ],
        help_text=_("Optional public rating displayed on the card"),
    )

    class Meta(TimeStampedModel.Meta):
        ordering = ("category", "name_en")
        verbose_name = _("menu item")
        verbose_name_plural = _("menu items")

    @property
    def name(self) -> str:
        return self.translate("name")

    @property
    def description(self) -> str:
        return self.translate("description")

    @property
    def highlight_badge(self) -> str:
        return self.translate("highlight_badge")

    def currency_symbol(self) -> str:
        symbols = {
            "USD": "$",
            "IRR": "﷼",
        }
        return symbols.get(self.currency, self.currency)

    def formatted_price(self) -> str:
        return f"{self.currency_symbol()}{format(self.price, '0.2f')}"

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs) -> None:
        if not self.slug:
            self.slug = slugify(self.name_en)
        super().save(*args, **kwargs)


