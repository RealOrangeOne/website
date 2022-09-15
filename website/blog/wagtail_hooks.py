from django.http.request import HttpRequest
from django.urls import reverse
from wagtail import hooks
from wagtail.admin.menu import MenuItem
from wagtail.admin.site_summary import SummaryItem

from .models import BlogPostListPage, BlogPostTagListPage


class BlogPostTagsMenuItem(MenuItem):
    url: str

    def __init__(self) -> None:
        super().__init__("Blog post tags", url="", icon_name="tag")

    def is_shown(self, request: HttpRequest) -> bool:
        if not self.url:
            blog_post_tag_list_id = (
                BlogPostTagListPage.objects.live().values_list("id", flat=True).first()
            )
            self.url = (
                reverse("wagtailadmin_explore", args=[blog_post_tag_list_id])
                if blog_post_tag_list_id
                else ""
            )

        return bool(self.url)


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


@hooks.register("register_admin_menu_item")
def register_blog_post_tags_menu_item() -> MenuItem:
    return BlogPostTagsMenuItem()


@hooks.register("construct_homepage_summary_items")
def register_blog_post_count_summary_item(request: HttpRequest, panels: list) -> None:
    panels.append(BlogPostCountSummaryItem(request))
