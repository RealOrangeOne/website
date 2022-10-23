from django.http.request import HttpRequest
from wagtail import hooks
from wagtail.admin.site_summary import SummaryItem

from .models import BlogPostListPage, BlogPostTagListPage


class BlogPostCountSummaryItem(SummaryItem):
    template_name = "blog/blog_post_count_summary_item.html"

    def is_shown(self) -> bool:
        return BlogPostListPage.objects.exists()

    def get_context_data(self, parent_context: dict) -> dict:
        context = super().get_context_data(parent_context)
        list_page = BlogPostListPage.objects.get()
        context["list_page"] = list_page
        context["posts"] = list_page.get_listing_pages().count()
        return context


class BlogPostTagsCountSummaryItem(SummaryItem):
    template_name = "blog/blog_post_tags_count_summary_item.html"

    def is_shown(self) -> bool:
        return BlogPostTagListPage.objects.exists()

    def get_context_data(self, parent_context: dict) -> dict:
        context = super().get_context_data(parent_context)
        list_page = BlogPostTagListPage.objects.get()
        context["list_page"] = list_page
        context["tags"] = list_page.get_listing_pages().count()
        return context


@hooks.register("construct_homepage_summary_items")
def register_blog_post_count_summary_item(request: HttpRequest, panels: list) -> None:
    panels.append(BlogPostCountSummaryItem(request))
    panels.append(BlogPostTagsCountSummaryItem(request))
