from datetime import timedelta
from math import ceil
from typing import Any, Optional

from django.core.paginator import EmptyPage, Paginator
from django.core.paginator import Page as PaginatorPage
from django.db import models
from django.http.request import HttpRequest
from django.http.response import Http404, HttpResponse, HttpResponseBadRequest
from django.shortcuts import redirect
from django.template.defaultfilters import pluralize
from django.utils.functional import cached_property, classproperty
from django.utils.text import Truncator, slugify
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.contrib.settings.models import BaseGenericSetting, register_setting
from wagtail.fields import RichTextField, StreamField
from wagtail.images import get_image_model_string
from wagtail.images.views.serve import generate_image_url
from wagtail.models import Page, PageQuerySet
from wagtail.search import index
from wagtail.snippets.blocks import SnippetChooserBlock
from wagtail.snippets.models import register_snippet
from wagtailmetadata.models import MetadataMixin

from website.contrib.unsplash.models import SIZES as UNSPLASH_SIZES
from website.contrib.unsplash.widgets import UnsplashPhotoChooser

from .serializers import PaginationSerializer
from .streamfield import add_heading_anchors, get_blocks, get_content_html
from .utils import (
    TocEntry,
    extend_query_params,
    extract_text,
    get_site_title,
    get_table_of_contents,
    get_url_mime_type,
)


class BasePage(Page):
    show_in_menus_default = True

    class Meta:
        abstract = True

    @classproperty
    def body_class(cls) -> str:  # noqa: N805
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
    def html_title_tag(self) -> str:
        return f"{self.html_title} :: {get_site_title()}"

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
    def show_table_of_contents(self) -> bool:
        return len(self.table_of_contents) >= 3

    @cached_property
    def reading_time(self) -> timedelta:
        """
        https://help.medium.com/hc/en-us/articles/214991667-Read-time
        """
        return timedelta(seconds=(self.word_count / 265) * 60)

    @cached_property
    def reading_time_display(self) -> str:
        reading_time_seconds = ceil(self.reading_time.total_seconds())

        # Show nothing if under a minute. Probably won't be shown anyway
        if reading_time_seconds < 60:
            return ""

        # If under an hour, show minutes
        if reading_time_seconds < 3600:
            minutes = ceil(reading_time_seconds / 60)

            return f"{minutes} minute{pluralize(minutes)}"

        # After that, show hours
        hours = ceil(reading_time_seconds / 60 / 60)
        return f"{hours} hour{pluralize(hours)}"

    @cached_property
    def show_reading_time(self) -> bool:
        """
        Only show reading time if it's longer than 2 minutes (rounded)
        """
        return ceil(self.reading_time.total_seconds() / 60) >= 2

    @cached_property
    def word_count(self) -> int:
        return len(self.plain_text.split())

    @cached_property
    def summary(self) -> str:
        return Truncator(self.plain_text).words(50)

    @cached_property
    def body_html(self) -> str:
        return add_heading_anchors(self._body_html)

    @cached_property
    def _body_html(self) -> str:
        return str(self.body)

    @cached_property
    def content_html(self) -> str:
        return get_content_html(self._body_html)

    @cached_property
    def plain_text(self) -> str:
        return extract_text(self.content_html).strip()

    def hero_url(
        self, image_size: str, wagtail_image_spec_extra: Optional[str] = None
    ) -> Optional[str]:
        if self.hero_unsplash_photo_id is not None:
            return self.hero_unsplash_photo.get_image_urls()[image_size]
        elif self.hero_image_id is not None:
            image_width = UNSPLASH_SIZES[image_size]
            wagtail_image_spec = f"width-{image_width}"
            if wagtail_image_spec_extra:
                wagtail_image_spec += wagtail_image_spec_extra
            return generate_image_url(self.hero_image, wagtail_image_spec)
        return None

    @cached_property
    def hero_image_urls(self) -> dict:
        return {
            int(width * 1.5): self.hero_url(size)
            for size, width in UNSPLASH_SIZES.items()
        }

    @cached_property
    def hero_image_url(self) -> Optional[str]:
        return self.hero_url("regular")

    @cached_property
    def list_image_url(self) -> Optional[str]:
        return self.hero_url("small")

    @cached_property
    def hero_image_alt(self) -> str:
        if self.hero_unsplash_photo_id is None:
            return ""

        return self.hero_unsplash_photo.data.get("description", "")

    def get_meta_url(self) -> str:
        return self.full_url

    def get_meta_image_url(self, request: HttpRequest) -> Optional[str]:
        return self.hero_url("regular", "|format-png")

    def get_meta_image_mime(self) -> Optional[str]:
        if self.hero_unsplash_photo_id is not None:
            return get_url_mime_type(self.hero_url("regular"))

        elif self.hero_image_id is not None:
            # We force these to PNG in `get_meta_image_url`
            return "image/png"

        return None

    def get_meta_title(self) -> str:
        return self.html_title

    def get_meta_description(self) -> str:
        return self.summary or self.get_meta_title()

    def get_object_title(self) -> str:
        return ""


class ContentPage(BaseContentPage):
    subpage_types: list[Any] = []


class BaseListingPage(RoutablePageMixin, BaseContentPage):
    PAGE_SIZE = 30
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
        return self.get_children().live().public().specific().order_by("title")

    def get_paginator_page(self) -> PaginatorPage:
        paginator = Paginator(self.get_listing_pages(), per_page=self.PAGE_SIZE)
        try:
            return paginator.page(self.serializer.validated_data["page"])
        except EmptyPage as e:
            raise Http404 from e

    def get_context(self, request: HttpRequest) -> dict:
        context = super().get_context(request)
        listing_pages = self.get_paginator_page()
        context["listing_pages"] = listing_pages

        # Show listing images if at least 1 page has an image
        context["show_listing_images"] = any(p.list_image_url for p in listing_pages)

        return context

    @cached_property
    def show_table_of_contents(self) -> bool:
        return False

    @cached_property
    def show_reading_time(self) -> bool:
        return False

    @route(r"^$")
    def index_route(self, request: HttpRequest) -> HttpResponse:
        self.serializer = PaginationSerializer(data=request.GET)
        if not self.serializer.is_valid():
            return HttpResponseBadRequest()
        return super().index_route(request)

    def get_meta_url(self) -> str:
        query_data = self.serializer.validated_data.copy()
        if query_data["page"] == 1:
            del query_data["page"]

        url = super().get_meta_url()

        return extend_query_params(url, query_data)

    @route(r"^feed/$")
    def feed(self, request: HttpRequest) -> HttpResponse:
        return redirect("feed", permanent=True)

    @route(r"^random/$")
    def random(self, request: HttpRequest) -> HttpResponse:
        page = self.get_listing_pages().order_by("?").first()
        if page is None:
            response = redirect(self.get_url(request=request), permanent=False)
        else:
            response = redirect(page.get_url(request=request), permanent=False)
        response.headers["X-Robots-Tag"] = "noindex"
        return response


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
class FooterSetting(BaseGenericSetting):
    icons = StreamField(
        [("icon", SnippetChooserBlock("contact.OnlineAccount", icon="user"))],
        use_json_field=True,
    )

    panels = [FieldPanel("icons")]

    class Meta:
        verbose_name = "Footer"
