from datetime import datetime, time

from django.contrib.syndication.views import Feed
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from wagtail.query import PageQuerySet

from .models import BlogPostPage


class BlogPostPageFeed(Feed):
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

    def item_title(self, item: BlogPostPage) -> str:
        return item.title

    def item_link(self, item: BlogPostPage) -> str:
        return item.get_full_url(request=self.request)

    def item_description(self, item: BlogPostPage) -> str:
        return item.summary

    def item_pubdate(self, item: BlogPostPage) -> datetime:
        return datetime.combine(item.date, time())

    def item_updateddate(self, item: BlogPostPage) -> datetime:
        return item.last_published_at
