from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.images import get_image_model_string

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
