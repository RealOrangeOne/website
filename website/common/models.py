from datetime import timedelta
from typing import Any, Optional

from django.core.cache import cache
from django.db import models
from django.dispatch import receiver
from django.http.request import HttpRequest
from django.utils.functional import cached_property, classproperty
from django.utils.text import slugify
from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField
from wagtail.images import get_image_model_string
from wagtail.images.views.serve import generate_image_url
from wagtail.models import Page, PageQuerySet
from wagtail.search import index
from wagtail.snippets.models import register_snippet
from wagtailmetadata.models import MetadataMixin

from website.common.utils import count_words
from website.contrib.unsplash.widgets import UnsplashPhotoChooser

from .streamfield import add_heading_anchors, get_blocks, get_content_html
from .utils import TocEntry, extract_text, get_table_of_contents, truncate_string


class BasePage(Page):
    show_in_menus_default = True

    class Meta:
        abstract = True

    @classproperty
    def body_class(cls) -> str:
        return "page-" + slugify(cls.__name__)

    def get_parent_pages(self) -> PageQuerySet:
        """
        Shim over the fact everything is in 1 tree
        """
        return self.get_ancestors().exclude(depth__lte=2)


class BaseContentPage(BasePage, MetadataMixin):
    subtitle = models.CharField(max_length=255, blank=True)
    hero_image = models.ForeignKey(
        get_image_model_string(), null=True, blank=True, on_delete=models.SET_NULL
    )
    hero_unsplash_photo = models.ForeignKey(
        "unsplash.UnsplashPhoto", null=True, blank=True, on_delete=models.SET_NULL
    )
    body = StreamField(get_blocks(), blank=True, use_json_field=True)

    content_panels = BasePage.content_panels + [
        FieldPanel("subtitle"),
        FieldPanel("hero_image"),
        FieldPanel("hero_unsplash_photo", widget=UnsplashPhotoChooser),
        FieldPanel("body"),
    ]

    search_fields = BasePage.search_fields + [
        index.SearchField("body"),
        index.SearchField("subtitle"),
    ]

    class Meta:
        abstract = True

    @cached_property
    def table_of_contents(self) -> list[TocEntry]:
        return get_table_of_contents(self.content_html)

    @cached_property
    def reading_time(self) -> timedelta:
        """
        https://help.medium.com/hc/en-us/articles/214991667-Read-time
        """
        return timedelta(seconds=(self.word_count / 265) * 60)

    @cached_property
    def show_reading_time(self) -> bool:
        """
        Only show reading time if it's longer than 2 minutes
        """
        return self.reading_time.total_seconds() >= 120

    @cached_property
    def word_count(self) -> int:
        return count_words(self.plain_text)

    @cached_property
    def summary(self) -> str:
        return truncate_string(self.plain_text, 50)

    @cached_property
    def body_html(self) -> str:
        return add_heading_anchors(self._body_html)

    @cached_property
    def body_html_cache_key(self) -> str:
        return f"body_html_{self.id}"

    @cached_property
    def _body_html(self) -> str:
        body_html = cache.get(self.body_html_cache_key)

        if body_html is None:
            body_html = str(self.body)

            # Cache for 1 day
            cache.set(self.body_html_cache_key, body_html, 86400)

        return body_html

    @cached_property
    def content_html(self) -> str:
        return get_content_html(self._body_html)

    @cached_property
    def plain_text(self) -> str:
        return extract_text(self.content_html)

    @cached_property
    def hero_image_url(self) -> Optional[str]:
        if self.hero_unsplash_photo_id is not None:
            return self.hero_unsplash_photo.get_image_urls()["regular"]
        elif self.hero_image_id is not None:
            return generate_image_url(self.hero_image, "width-1200")
        return None

    @cached_property
    def list_image_url(self) -> Optional[str]:
        if self.hero_unsplash_photo_id is not None:
            return self.hero_unsplash_photo.get_image_urls()["small"]
        elif self.hero_image_id is not None:
            return generate_image_url(self.hero_image, "width-400")
        return None

    def get_meta_url(self) -> str:
        return self.full_url

    def get_meta_image_url(self, request: HttpRequest) -> Optional[str]:
        return self.hero_image_url

    def get_meta_title(self) -> str:
        return self.seo_title or self.title

    def get_meta_description(self) -> str:
        return self.summary

    def get_object_title(self) -> str:
        return ""


@receiver(models.signals.post_save)
def clear_body_html_cache(sender: Any, instance: models.Model, **kwargs: dict) -> None:
    if isinstance(instance, BaseContentPage):
        cache.delete(instance.body_html_cache_key)


class ContentPage(BaseContentPage):
    subpage_types: list[Any] = []


class ListingPage(BaseContentPage):
    def get_context(self, request: HttpRequest) -> dict:
        context = super().get_context(request)
        context["child_pages"] = (
            self.get_children()
            .live()
            .specific()
            .select_related("hero_image")
            .select_related("hero_unsplash_photo")
        )
        return context


@register_snippet
class ReferralLink(models.Model, index.Indexed):
    url = models.URLField()
    name = models.CharField(max_length=64, unique=True)

    panels = [
        FieldPanel("name"),
        FieldPanel("url"),
    ]

    search_fields = [index.AutocompleteField("name"), index.SearchField("url")]

    def __str__(self) -> str:
        return self.name
