from django.db import models
from django.http.request import HttpRequest
from wagtail.admin.panels import FieldPanel
from wagtail.images import get_image_model_string

from website.blog.models import BlogPostPage
from website.common.models import BasePage


class HomePage(BasePage):
    max_count = 1

    heading = models.CharField(max_length=128, blank=True)
    image = models.ForeignKey(
        get_image_model_string(), null=True, on_delete=models.SET_NULL
    )

    content_panels = BasePage.content_panels + [
        FieldPanel("heading"),
        FieldPanel("image"),
    ]

    def get_context(self, request: HttpRequest) -> dict:
        context = super().get_context(request)
        context["latest_blog_post"] = (
            BlogPostPage.objects.live()  # type:ignore[attr-defined]
            .defer_streamfields()
            .order_by("-date")
            .first()
        )
        return context
