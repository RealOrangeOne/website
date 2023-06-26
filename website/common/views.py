from datetime import datetime
from typing import Any, Optional

from django.contrib.syndication.views import Feed
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_control, cache_page
from django.views.defaults import ERROR_404_TEMPLATE_NAME
from django.views.generic import TemplateView
from wagtail.models import Page
from wagtail.query import PageQuerySet

from website.contrib.singleton_page.utils import SingletonPageCache
from website.home.models import HomePage
from website.search.models import SearchPage

from .models import BaseContentPage, BasePage


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
    link = "/feed/"
    title = "All pages feed"

    @method_decorator(cache_page(60 * 60))
    def __call__(
        self, request: HttpRequest, *args: list, **kwargs: dict
    ) -> HttpResponse:
        self.request = request
        return super().__call__(request, *args, **kwargs)

    def items(self) -> PageQuerySet:
        return Page.objects.live().public().exclude(depth__lte=2)

    def item_title(self, item: BasePage) -> str:
        return item.title

    def item_link(self, item: BasePage) -> str:
        return item.get_full_url(request=self.request)

    def item_pubdate(self, item: BasePage) -> datetime:
        return item.first_published_at

    def item_updateddate(self, item: BasePage) -> datetime:
        return item.last_published_at


class ContentPageFeed(AllPagesFeed):
    def __init__(self, posts: PageQuerySet, link: str, title: str):
        self.posts = posts
        self.link = link
        self.title = title
        super().__init__()

    def items(self) -> PageQuerySet:
        return self.posts

    def item_description(self, item: BaseContentPage) -> str:
        return item.summary

    def item_pubdate(self, item: BaseContentPage) -> datetime:
        return item.first_published_at

    def item_updateddate(self, item: BaseContentPage) -> datetime:
        return item.last_published_at

    def item_enclosure_url(self, item: BaseContentPage) -> Optional[str]:
        hero_image_url = item.hero_image_url()

        if hero_image_url and hero_image_url.startswith("/"):
            return self.request.build_absolute_uri(hero_image_url)

        return hero_image_url

    def item_enclosure_mime_type(self, item: BaseContentPage) -> str:
        return ""

    def item_enclosure_length(self, item: BaseContentPage) -> int:
        return 0
