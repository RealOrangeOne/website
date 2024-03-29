from django.db import models
from django.http.request import HttpRequest
from wagtail.admin.panels import FieldPanel
from wagtail.images import get_image_model_string
from wagtail.images.models import Image
from wagtailmetadata.models import WagtailImageMetadataMixin

from website.common.models import BasePage
from website.contrib.singleton_page.utils import SingletonPageCache


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
        from website.blog.models import BlogPostListPage, BlogPostPage
        from website.search.models import SearchPage

        context = super().get_context(request)
        context["recent_posts"] = list(
            BlogPostPage.objects.live()
            .public()
            .defer_streamfields()
            .order_by("-date")[:7]
        )
        context["latest_blog_post"] = (
            context["recent_posts"].pop(0) if context["recent_posts"] else None
        )
        context["search_page_url"] = SingletonPageCache.get_url(SearchPage, request)
        context["blog_post_list_url"] = SingletonPageCache.get_url(
            BlogPostListPage, request
        )

        return context
