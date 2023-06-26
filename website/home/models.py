from typing import Optional, Tuple

from django.db import models
from django.http.request import HttpRequest
from django_cache_decorator import django_cache_decorator
from wagtail.admin.panels import FieldPanel
from wagtail.images import get_image_model_string
from wagtail.images.models import Image
from wagtailmetadata.models import WagtailImageMetadataMixin

from website.common.models import BasePage
from website.contrib.singleton_page.utils import SingletonPageCache


@django_cache_decorator(time=600)
def get_latest_blog_post() -> Optional[Tuple[str, str]]:
    from website.blog.models import BlogPostPage

    try:
        latest_blog_post = (
            BlogPostPage.objects.live().public().defer_streamfields().latest("date")
        )
    except BlogPostPage.DoesNotExist:
        return None

    return latest_blog_post.title, latest_blog_post.get_url()


class HomePage(BasePage, WagtailImageMetadataMixin):
    max_count = 1

    heading = models.CharField(max_length=128, blank=True)
    image = models.ForeignKey(
        get_image_model_string(), null=True, on_delete=models.SET_NULL
    )

    content_panels = BasePage.content_panels + [
        FieldPanel("heading"),
        FieldPanel("image"),
    ]

    def get_meta_url(self) -> str:
        return self.full_url

    def get_meta_image(self) -> Image | None:
        return self.image

    def get_meta_title(self) -> str:
        return self.seo_title or self.title

    def get_meta_description(self) -> str:
        return self.search_description

    def get_object_title(self) -> str:
        return self.html_title

    def get_context(self, request: HttpRequest) -> dict:
        from website.search.models import SearchPage

        context = super().get_context(request)
        context["latest_blog_post"] = get_latest_blog_post()
        context["search_page_url"] = SingletonPageCache.get_url(SearchPage, request)
        return context
