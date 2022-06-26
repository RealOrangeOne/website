from typing import Any

from django.db import models
from django.http.request import HttpRequest
from django.utils.functional import cached_property, classproperty
from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField
from wagtail.images import get_image_model_string
from wagtail.models import Page

from .streamfield import get_blocks
from .utils import TocEntry, get_table_of_contents


class BasePage(Page):
    show_in_menus_default = True

    HERO_IMAGE_SIZE = "width-1200"

    class Meta:
        abstract = True

    @classproperty
    def body_class(cls) -> str:
        return "page-" + cls._meta.db_table.replace("_", "-")

    def get_parent_pages(self) -> models.QuerySet[Page]:
        """
        Shim over the fact everything is in 1 tree
        """
        return self.get_ancestors().reverse().exclude(depth__lte=2)


class BaseContentMixin(models.Model):
    subtitle = models.CharField(max_length=255, blank=True)
    hero_image = models.ForeignKey(
        get_image_model_string(), null=True, blank=True, on_delete=models.SET_NULL
    )
    body = StreamField(get_blocks(), blank=True, use_json_field=True)

    content_panels = [
        FieldPanel("subtitle"),
        FieldPanel("hero_image"),
        FieldPanel("body"),
    ]

    class Meta:
        abstract = True

    @cached_property
    def table_of_contents(self) -> list[TocEntry]:
        return get_table_of_contents()

    @cached_property
    def reading_time(self) -> int:
        return 4

    @cached_property
    def word_count(self) -> int:
        return 1600


class ContentPage(BasePage, BaseContentMixin):  # type: ignore[misc]
    subpage_types: list[Any] = []
    content_panels = BasePage.content_panels + BaseContentMixin.content_panels


class ListingPage(BasePage, BaseContentMixin):  # type: ignore[misc]
    content_panels = BasePage.content_panels + BaseContentMixin.content_panels

    def get_context(self, request: HttpRequest) -> dict:
        context = super().get_context(request)
        context["child_pages"] = (
            self.get_children().live().specific().select_related("hero_image")
        )
        return context
