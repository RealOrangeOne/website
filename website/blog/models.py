from typing import Any

from django.http.request import HttpRequest

from website.common.models import BaseContentMixin, BasePage


class BlogListPage(BaseContentMixin, BasePage):  # type: ignore[misc]
    max_count = 1
    subpage_types = ["blog.BlogPostPage"]
    content_panels = BasePage.content_panels + BaseContentMixin.content_panels

    def get_context(self, request: HttpRequest) -> dict:
        context = super().get_context(request)
        context["child_pages"] = (
            self.get_children().live().specific().select_related("hero_image")
        )
        return context


class BlogPostPage(BaseContentMixin, BasePage):  # type: ignore[misc]
    subpage_types: list[Any] = []
    parent_page_types = [BlogListPage]
    content_panels = BasePage.content_panels + BaseContentMixin.content_panels
