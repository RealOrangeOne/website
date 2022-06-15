from django.db import models
from django.utils.functional import classproperty
from wagtail.admin.panels import FieldPanel
from wagtail.images import get_image_model_string
from wagtail.models import Page


class BasePage(Page):
    class Meta:
        abstract = True

    @classproperty
    def body_class(cls) -> str:
        return "page-" + cls._meta.db_table.replace("_", "-")


class ContentPage(BasePage):
    subtitle = models.CharField(max_length=255, blank=True)
    hero_image = models.ForeignKey(
        get_image_model_string(), null=True, on_delete=models.SET_NULL
    )

    content_panels = BasePage.content_panels + [
        FieldPanel("subtitle"),
        FieldPanel("hero_image"),
    ]
