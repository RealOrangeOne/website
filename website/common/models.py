from django.db import models
from django.utils.functional import classproperty
from wagtail.admin.panels import FieldPanel
from wagtail.models import Page


class BasePage(Page):
    class Meta:
        abstract = True

    @classproperty
    def body_class(cls) -> str:
        return "page-" + cls._meta.db_table.replace("_", "-")


class ContentPage(BasePage):
    subtitle = models.CharField(max_length=255, blank=True)

    content_panels = BasePage.content_panels + [FieldPanel("subtitle")]
