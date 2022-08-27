from datetime import datetime
from typing import Any

from django.contrib.syndication.views import Feed
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.urls import reverse
from django.views.defaults import ERROR_404_TEMPLATE_NAME
from django.views.generic import TemplateView
from wagtail.models import Page
from wagtail.query import PageQuerySet

from website.home.models import HomePage

from .models import BaseContentPage, BasePage


class Error404View(TemplateView):
    template_name = ERROR_404_TEMPLATE_NAME

    def render_to_response(self, context: dict, **response_kwargs: Any) -> HttpResponse:
        if self.request.resolver_match.url_name != "404":
            response_kwargs["status"] = 404
        return super().render_to_response(context, **response_kwargs)

    def get_context_data(self, **kwargs: dict) -> dict:
        context = super().get_context_data(**kwargs)
        context["homepage"] = HomePage.objects.live().get()
        return context


page_not_found = Error404View.as_view()


class RobotsView(TemplateView):
    template_name = "robots.txt"
    content_type = "text/plain"

    def get_context_data(self, **kwargs: dict) -> dict:
        context = super().get_context_data(**kwargs)
        context["sitemap"] = self.request.build_absolute_uri(reverse("sitemap"))
        return context


class KeybaseView(TemplateView):
    template_name = "keybase.txt"
    content_type = "text/plain"


class AllPagesFeed(Feed):
    link = "/feed/"
    title = "All pages feed"

    def __call__(
        self, request: HttpRequest, *args: list, **kwargs: dict
    ) -> HttpResponse:
        self.request = request
        return super().__call__(request, *args, **kwargs)

    def items(self) -> PageQuerySet:
        return Page.objects.live().exclude(depth__lte=2)

    def item_title(self, item: BasePage) -> str:
        return item.title

    def item_link(self, item: BasePage) -> str:
        return item.get_full_url(request=self.request)

    def item_pubdate(self, item: BasePage) -> datetime:
        return item.first_published_at

    def item_updateddate(self, item: BasePage) -> datetime:
        return item.last_published_at


class ContentPageFeed(Feed):
    def __init__(self, posts: PageQuerySet, link: str, title: str):
        self.posts = posts
        self.link = link
        self.title = title
        super().__init__()

    def __call__(
        self, request: HttpRequest, *args: list, **kwargs: dict
    ) -> HttpResponse:
        self.request = request
        return super().__call__(request, *args, **kwargs)

    def items(self) -> PageQuerySet:
        return self.posts

    def item_title(self, item: BaseContentPage) -> str:
        return item.title

    def item_link(self, item: BaseContentPage) -> str:
        return item.get_full_url(request=self.request)

    def item_description(self, item: BaseContentPage) -> str:
        return item.summary

    def item_pubdate(self, item: BaseContentPage) -> datetime:
        return item.first_published_at

    def item_updateddate(self, item: BaseContentPage) -> datetime:
        return item.last_published_at
