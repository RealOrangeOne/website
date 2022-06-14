from django.db import models
from wagtail.admin.panels import FieldPanel

from website.common.models import BasePage


class HomePage(BasePage):
    max_count = 1

    heading = models.CharField(max_length=128, blank=True)

    content_panels = BasePage.content_panels + [FieldPanel("heading")]
