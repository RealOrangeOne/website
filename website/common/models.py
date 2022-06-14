from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.models import Page


class BasePage(Page):
    class Meta:
        abstract = True

    @classmethod
    @property
    def body_class(cls) -> str:
        return "page-" + cls._meta.db_table.replace("_", "-")


class ContentPage(BasePage):
    subtitle = models.CharField(max_length=255, blank=True)

    content_panels = BasePage.content_panels + [FieldPanel("subtitle")]
