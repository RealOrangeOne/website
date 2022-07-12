from typing import Any

from django.db import models
from django.db.models.functions import TruncMonth
from django.http.request import HttpRequest
from django.utils import timezone
from django.utils.functional import cached_property
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey
from taggit.models import ItemBase, TagBase
from wagtail.admin.panels import FieldPanel
from wagtail.query import PageQuerySet

from website.common.models import BaseContentMixin, BasePage
from website.common.utils import TocEntry


class BlogListPage(BaseContentMixin, BasePage):  # type: ignore[misc]
    max_count = 1
    subpage_types = ["blog.BlogPostPage"]
    content_panels = BasePage.content_panels + BaseContentMixin.content_panels

    @cached_property
    def reading_time(self) -> int:
        """
        How does one read a list page?
        """
        return 0

    @cached_property
    def table_of_contents(self) -> list[TocEntry]:
        post_months = [
            dt.strftime("%Y-%m")
            for dt in self.get_children()
            .live()
            .annotate(post_month=TruncMonth("date", output_field=models.DateField()))
            .order_by("-post_month")
            .values_list("post_month", flat=True)
            .distinct()
        ]

        return [TocEntry(post_month, post_month, 0, []) for post_month in post_months]

    def get_children(self) -> PageQuerySet:
        """
        Since the children are always `BlogPostPage`, so juts use the specific queryset to save the `JOIN`.
        """
        return BlogPostPage.objects.child_of(self)  # type: ignore[attr-defined]

    def get_context(self, request: HttpRequest) -> dict:
        context = super().get_context(request)
        context["child_pages"] = (
            self.get_children()
            .live()
            .select_related("hero_image")
            .select_related("hero_unsplash_photo")
            .prefetch_related("tags")
            .order_by("-date")
        )
        return context


class BlogPostTag(TagBase):
    free_tagging = False

    panels = [FieldPanel("name")]

    class Meta:
        verbose_name = "blog tag"
        verbose_name_plural = "blog tags"


class TaggedBlog(ItemBase):
    tag = models.ForeignKey(
        BlogPostTag, related_name="tagged_blogs", on_delete=models.CASCADE
    )
    content_object = ParentalKey(
        "blog.BlogPostPage", on_delete=models.CASCADE, related_name="tagged_items"
    )


class BlogPostPage(BaseContentMixin, BasePage):  # type: ignore[misc]
    subpage_types: list[Any] = []
    parent_page_types = [BlogListPage]

    tags = ClusterTaggableManager(through=TaggedBlog, blank=True)
    date = models.DateField(default=timezone.now)

    content_panels = (
        BasePage.content_panels
        + BaseContentMixin.content_panels
        + [FieldPanel("date"), FieldPanel("tags")]
    )
