from datetime import datetime, time
from typing import Any, Optional

from django.contrib.syndication.views import Feed
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.templatetags.static import static
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_control, cache_page
from django.views.defaults import ERROR_404_TEMPLATE_NAME
from django.views.generic import RedirectView, TemplateView
from wagtail.models import Page
from wagtail.query import PageQuerySet
from wagtail_favicon.models import FaviconSettings
from wagtail_favicon.utils import get_rendition_url

from website.blog.models import BlogPostPage
from website.common.utils import get_site_title
from website.contrib.singleton_page.utils import SingletonPageCache
from website.home.models import HomePage
from website.search.models import SearchPage

from .feed_generators import CustomFeed
from .models import BaseListingPage, BasePage


class Error404View(TemplateView):
    template_name = ERROR_404_TEMPLATE_NAME

    def render_to_response(self, context: dict, **response_kwargs: Any) -> HttpResponse:
        resolver_match = self.request.resolver_match
        if not resolver_match or resolver_match.url_name != "404":
            response_kwargs["status"] = 404
        return super().render_to_response(context, **response_kwargs)

    def get_context_data(self, **kwargs: dict) -> dict:
        context = super().get_context_data(**kwargs)
        context["homepage"] = HomePage.objects.get()
        context["search_url"] = SingletonPageCache.get_url(SearchPage, self.request)
        return context


page_not_found = Error404View.as_view()


@method_decorator(cache_control(max_age=60 * 60), name="dispatch")
class RobotsView(TemplateView):
    template_name = "robots.txt"
    content_type = "text/plain"

    def get_context_data(self, **kwargs: dict) -> dict:
        context = super().get_context_data(**kwargs)
        context["sitemap"] = self.request.build_absolute_uri(reverse("sitemap"))
        return context


@method_decorator(cache_control(max_age=60 * 60), name="dispatch")
class KeybaseView(TemplateView):
    template_name = "keybase.txt"
    content_type = "text/plain"


class AllPagesFeed(Feed):
    feed_type = CustomFeed
    link = "/"
    description_template = "feed-description.html"

    def __init__(self) -> None:
        self.style_tag = f'<?xml-stylesheet href="{static("contrib/pretty-feed-v3.xsl")}" type="text/xsl"?>'.encode()
        super().__init__()

    @method_decorator(cache_page(60 * 60))
    def __call__(
        self, request: HttpRequest, *args: list, **kwargs: dict
    ) -> HttpResponse:
        self.request = request
        response = super().__call__(request, *args, **kwargs)

        # Override Content-Type to allow styles
        response.headers["content-type"] = "application/xml"

        # Inject styles
        opening_xml = response.content.find(b"?>") + 2
        response.content = (
            response.content[:opening_xml]
            + b"\n"
            + self.style_tag
            + response.content[opening_xml:]
        )

        return response

    def feed_extra_kwargs(self, obj: None) -> dict:
        return {**super().feed_extra_kwargs(obj), "request": self.request}

    def title(self) -> str:
        return f"Feed :: {get_site_title()}"

    def items(self) -> PageQuerySet:
        return (
            Page.objects.live()
            .public()
            .exclude(depth__lte=2)
            .not_type(BaseListingPage)
            .specific()
            .order_by("-last_published_at")
        )

    def item_guid(self, item: BasePage) -> str:
        return item.get_full_url(request=self.request)

    def item_title(self, item: BasePage) -> str:
        return item.title

    def item_link(self, item: BasePage) -> str:
        return item.get_full_url(request=self.request) + "?utm_medium=rss"

    def item_pubdate(self, item: BasePage) -> datetime:
        if item_date := getattr(item, "date", None):
            return datetime.combine(item_date, time())
        return item.first_published_at

    def item_updateddate(self, item: BasePage) -> datetime:
        return item.last_published_at

    def item_categories(self, item: BasePage) -> Optional[list[str]]:
        if isinstance(item, BlogPostPage):
            return item.tags_list.values_list("slug", flat=True)
        return None

    def item_enclosure_url(self, item: BasePage) -> Optional[str]:
        if not hasattr(item, "get_meta_image_url"):
            return ""

        image_url = item.get_meta_image_url(self.request)

        if image_url and image_url.startswith("/"):
            return self.request.build_absolute_uri(image_url)

        return image_url

    def item_enclosure_mime_type(self, item: BasePage) -> str:
        if not hasattr(item, "get_meta_image_mime"):
            return ""

        return item.get_meta_image_mime() or ""

    item_enclosure_length = 0


@method_decorator(cache_control(max_age=60 * 60), name="dispatch")
class FaviconView(RedirectView):
    def get_redirect_url(self) -> str:
        favicon_settings = FaviconSettings.for_request(self.request)
        size = FaviconSettings.icon_sizes[0]

        # Force image to PNG
        return get_rendition_url(
            favicon_settings.base_favicon_image, f"fill-{size}|format-png"
        )
