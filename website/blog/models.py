from typing import Any

from django.db import models
from django.db.models.functions import TruncMonth
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.utils import timezone
from django.utils.functional import cached_property
from modelcluster.fields import ParentalManyToManyField
from wagtail.admin.panels import FieldPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.query import PageQuerySet

from website.common.models import BaseContentPage
from website.common.utils import TocEntry


class BlogPostListPage(RoutablePageMixin, BaseContentPage):
    max_count = 1
    subpage_types = [
        "blog.BlogPostPage",
        "blog.BlogPostTagListPage",
        "blog.BlogPostCollectionListPage",
        "blog.BlogPostCollectionPage",
    ]

    @cached_property
    def show_reading_time(self) -> bool:
        return False

    @cached_property
    def table_of_contents(self) -> list[TocEntry]:
        post_months = [
            dt.strftime("%Y-%m")
            for dt in self.get_blog_posts()
            .annotate(post_month=TruncMonth("date", output_field=models.DateField()))
            .order_by("-post_month")
            .values_list("post_month", flat=True)
            .distinct()
        ]

        return [TocEntry(post_month, post_month, 0, []) for post_month in post_months]

    def get_blog_posts(self) -> PageQuerySet:
        return BlogPostPage.objects.descendant_of(self).live()

    def get_context(self, request: HttpRequest) -> dict:
        context = super().get_context(request)
        context["child_pages"] = (
            self.get_blog_posts()
            .select_related("hero_image")
            .select_related("hero_unsplash_photo")
            .prefetch_related("tags")
            .order_by("-date")
        )
        return context

    @route(r"^feed/$")
    def feed(self, request: HttpRequest) -> HttpResponse:
        from .views import BlogPostPageFeed

        return BlogPostPageFeed(
            self.get_blog_posts().order_by("-date"), self.get_url(), self.title
        )(request)


class BlogPostPage(BaseContentPage):
    subpage_types: list[Any] = []
    parent_page_types = [BlogPostListPage, "blog.BlogPostCollectionPage"]

    tags = ParentalManyToManyField("blog.BlogPostTagPage", blank=True)
    date = models.DateField(default=timezone.now)

    content_panels = BaseContentPage.content_panels + [
        FieldPanel("date"),
        FieldPanel("tags"),
    ]


class BlogPostTagListPage(BaseContentPage):
    max_count = 1
    parent_page_types = [BlogPostListPage]
    subpage_types = ["blog.BlogPostTagPage"]

    @cached_property
    def table_of_contents(self) -> list[TocEntry]:
        return [TocEntry(page.title, page.slug, 0, []) for page in self.get_tags()]

    def get_tags(self) -> PageQuerySet:
        return (
            self.get_children()
            .specific()
            .live()
            .order_by("title")
            .select_related("hero_image")
            .select_related("hero_unsplash_photo")
        )

    def get_context(self, request: HttpRequest) -> dict:
        context = super().get_context(request)
        context["tags"] = self.get_children().specific().live().order_by("title")
        return context


class BlogPostTagPage(RoutablePageMixin, BaseContentPage):
    subpage_types: list[Any] = []
    parent_page_types = [BlogPostTagListPage]

    @cached_property
    def table_of_contents(self) -> list[TocEntry]:
        return [
            TocEntry(page.title, page.slug, 0, []) for page in self.get_blog_posts()
        ]

    def get_blog_posts(self) -> PageQuerySet:
        blog_list_page = BlogPostListPage.objects.all().live().get()
        return (
            blog_list_page.get_blog_posts()
            .filter(tags=self)
            .order_by("-date")
            .select_related("hero_image")
            .select_related("hero_unsplash_photo")
        )

    def get_context(self, request: HttpRequest) -> dict:
        context = super().get_context(request)
        context["pages"] = self.get_blog_posts()
        return context

    @route(r"^feed/$")
    def feed(self, request: HttpRequest) -> HttpResponse:
        from .views import BlogPostPageFeed

        return BlogPostPageFeed(
            self.get_blog_posts().order_by("-date"), self.get_url(), self.title
        )(request)


class BlogPostCollectionListPage(BaseContentPage):
    subpage_types: list[Any] = []
    parent_page_types = [BlogPostListPage]
    max_count = 1

    @cached_property
    def table_of_contents(self) -> list[TocEntry]:
        return [
            TocEntry(page.title, page.slug, 0, []) for page in self.get_collections()
        ]

    def get_collections(self) -> PageQuerySet:
        blog_list_page = BlogPostListPage.objects.all().live().get()
        return BlogPostCollectionPage.objects.child_of(blog_list_page).live()

    def get_context(self, request: HttpRequest) -> dict:
        context = super().get_context(request)
        context["collections"] = self.get_collections()
        return context


class BlogPostCollectionPage(BaseContentPage):
    parent_page_types = [BlogPostListPage]
    subpage_types = [BlogPostPage]

    @cached_property
    def table_of_contents(self) -> list[TocEntry]:
        return [
            TocEntry(page.title, page.slug, 0, []) for page in self.get_blog_posts()
        ]

    def get_blog_posts(self) -> PageQuerySet:
        return (
            BlogPostPage.objects.child_of(self)
            .order_by("-date")
            .select_related("hero_image")
            .select_related("hero_unsplash_photo")
        )

    def get_context(self, request: HttpRequest) -> dict:
        context = super().get_context(request)
        context["pages"] = self.get_blog_posts()
        return context
