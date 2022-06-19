from typing import Any

from django.db import models
from django.utils.functional import classproperty
from wagtail.admin.panels import FieldPanel
from wagtail.images import get_image_model_string
from wagtail.models import Page


class BasePage(Page):
    show_in_menus_default = True

    HERO_IMAGE_SIZE = "width-1200"

    class Meta:
        abstract = True

    @classproperty
    def body_class(cls) -> str:
        return "page-" + cls._meta.db_table.replace("_", "-")


class BaseContentMixin(models.Model):
    subtitle = models.CharField(max_length=255, blank=True)
    hero_image = models.ForeignKey(
        get_image_model_string(), null=True, blank=True, on_delete=models.SET_NULL
    )

    content_panels = [
        FieldPanel("subtitle"),
        FieldPanel("hero_image"),
    ]

    class Meta:
        abstract = True


class ContentPage(BasePage, BaseContentMixin):  # type: ignore[misc]
    subpage_types: list[Any] = []
    content_panels = BasePage.content_panels + BaseContentMixin.content_panels


class ListingPage(BasePage, BaseContentMixin):  # type: ignore[misc]
    content_panels = BasePage.content_panels + BaseContentMixin.content_panels
