from typing import Any

from django.db import models
from django.http.request import HttpRequest
from django.utils import timezone
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey
from taggit.models import ItemBase, TagBase
from wagtail.admin.panels import FieldPanel

from website.common.models import BaseContentMixin, BasePage


class BlogListPage(BaseContentMixin, BasePage):  # type: ignore[misc]
    max_count = 1
    subpage_types = ["blog.BlogPostPage"]
    content_panels = BasePage.content_panels + BaseContentMixin.content_panels

    def get_context(self, request: HttpRequest) -> dict:
        context = super().get_context(request)
        context["child_pages"] = (
            self.get_children()
            .live()
            .specific()
            .select_related("hero_image")
            .prefetch_related("tags")
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
