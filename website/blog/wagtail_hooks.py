from django.http.request import HttpRequest
from django.urls import reverse
from wagtail import hooks
from wagtail.admin.menu import MenuItem

from .models import BlogPostTagListPage


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


@hooks.register("register_admin_menu_item")
def register_blog_post_tags_menu_item() -> MenuItem:
    return BlogPostTagsMenuItem()
