from django.urls import reverse
from wagtail import hooks
from wagtail.admin.menu import MenuItem

from .models import BlogPostTagListPage


@hooks.register("register_admin_menu_item")
def register_blog_post_tags_menu_item() -> MenuItem:
    blog_post_tag_list_id = (
        BlogPostTagListPage.objects.live()  # type:ignore[attr-defined]
        .values_list("id", flat=True)
        .get()
    )
    return MenuItem(
        "Blog post tags",
        reverse("wagtailadmin_explore", args=[blog_post_tag_list_id]),
        icon_name="tag",
    )
