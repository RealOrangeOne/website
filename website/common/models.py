from datetime import timedelta
from typing import Any, Optional, Type

from django.contrib.syndication.views import Feed
from django.core.paginator import EmptyPage
from django.core.paginator import Page as PaginatorPage
from django.core.paginator import Paginator
from django.db import models
from django.http.request import HttpRequest
from django.http.response import Http404, HttpResponse, HttpResponseBadRequest
from django.utils.decorators import method_decorator
from django.utils.functional import cached_property, classproperty
from django.utils.text import slugify
from django.views.decorators.cache import cache_page
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.contrib.settings.models import BaseSetting, register_setting
from wagtail.fields import RichTextField, StreamField
from wagtail.images import get_image_model_string
from wagtail.images.views.serve import generate_image_url
from wagtail.models import Page, PageQuerySet
from wagtail.search import index
from wagtail.snippets.blocks import SnippetChooserBlock
from wagtail.snippets.models import register_snippet
from wagtailmetadata.models import MetadataMixin

from website.contrib.unsplash.widgets import UnsplashPhotoChooser
from website.utils.cache import cached_model_property

from .serializers import PaginationSerializer
from .streamfield import add_heading_anchors, get_blocks, get_content_html
from .utils import (
    TocEntry,
    count_words,
    extract_text,
    get_table_of_contents,
    prefetch_for_listing,
    truncate_string,
)


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

    @cached_property
    def html_title(self) -> str:
        return self.seo_title or self.title

    @cached_property
    def hero_title(self) -> str:
        return self.html_title


class BaseContentPage(BasePage, MetadataMixin):
    subtitle = RichTextField(blank=True, editor="plain")
    hero_image = models.ForeignKey(
        get_image_model_string(), null=True, blank=True, on_delete=models.SET_NULL
    )
    hero_unsplash_photo = models.ForeignKey(
        "unsplash.UnsplashPhoto", null=True, blank=True, on_delete=models.SET_NULL
    )
    body = StreamField(get_blocks(), blank=True, use_json_field=True)

    content_panels = BasePage.content_panels + [
        FieldPanel("subtitle"),
        MultiFieldPanel(
            [
                FieldPanel("hero_image"),
                FieldPanel("hero_unsplash_photo", widget=UnsplashPhotoChooser),
            ],
            heading="Hero image",
        ),
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
    def _body_html(self) -> str:
        return str(self.body)

    @cached_model_property
    def content_html(self) -> str:
        return get_content_html(self._body_html)

    @cached_model_property
    def plain_text(self) -> str:
        return extract_text(self.content_html)

    def hero_url(self, unsplash_size: str, wagtail_image_spec: str) -> Optional[str]:
        if self.hero_unsplash_photo_id is not None:
            return self.hero_unsplash_photo.get_image_urls()[unsplash_size]
        elif self.hero_image_id is not None:
            return generate_image_url(self.hero_image, wagtail_image_spec)
        return None

    @cached_property
    def hero_image_url(self) -> Optional[str]:
        return self.hero_url("full", "width-2000")

    @cached_property
    def list_image_url(self) -> Optional[str]:
        return self.hero_url("small", "width-400")

    def get_meta_url(self) -> str:
        return self.full_url

    def get_meta_image_url(self, request: HttpRequest) -> Optional[str]:
        return self.hero_url("regular", "width-1000|format-png")

    def get_meta_title(self) -> str:
        return self.html_title

    def get_meta_description(self) -> str:
        return self.summary

    def get_object_title(self) -> str:
        return ""


class ContentPage(BaseContentPage):
    subpage_types: list[Any] = []


class BaseListingPage(RoutablePageMixin, BaseContentPage):
    PAGE_SIZE = 20
    subtitle = None

    content_panels = [
        panel
        for panel in BaseContentPage.content_panels
        if getattr(panel, "field_name", None) != "subtitle"
    ]

    search_fields = [
        panel
        for panel in BaseContentPage.search_fields
        if getattr(panel, "field_name", None) != "subtitle"
    ]

    class Meta:
        abstract = True

    def get_listing_pages(self) -> models.QuerySet:
        return prefetch_for_listing(
            self.get_children().live().public().specific().order_by("title")
        )

    def get_paginator_page(self) -> PaginatorPage:
        paginator = Paginator(self.get_listing_pages(), per_page=self.PAGE_SIZE)
        try:
            return paginator.page(self.serializer.validated_data["page"])
        except EmptyPage:
            raise Http404

    def get_context(self, request: HttpRequest) -> dict:
        context = super().get_context(request)
        context["listing_pages"] = self.get_paginator_page()
        return context

    @cached_property
    def table_of_contents(self) -> list[TocEntry]:
        return []

    @cached_property
    def show_reading_time(self) -> bool:
        return False

    @property
    def feed_class(self) -> Type[Feed]:
        from .views import ContentPageFeed

        return ContentPageFeed

    @route(r"^$")
    def index_route(self, request: HttpRequest) -> HttpResponse:
        self.serializer = PaginationSerializer(data=request.GET)
        if not self.serializer.is_valid():
            return HttpResponseBadRequest()
        return super().index_route(request)

    @route(r"^feed/$")
    @method_decorator(cache_page(60 * 30))
    def feed(self, request: HttpRequest) -> HttpResponse:
        return self.feed_class(
            self.get_listing_pages(),
            self.get_full_url(request),
            self.html_title,
        )(request)


class ListingPage(BaseListingPage):
    pass


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


@register_setting(icon="arrow-down")
class FooterSetting(BaseSetting):
    icons = StreamField(
        [("icon", SnippetChooserBlock("contact.OnlineAccount", icon="user"))]
    )

    panels = [FieldPanel("icons")]

    class Meta:
        verbose_name = "Footer"
