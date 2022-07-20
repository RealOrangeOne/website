from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.snippets.models import register_snippet


@register_snippet
class OnlineAccount(models.Model):
    name = models.CharField(max_length=64, unique=True)
    url = models.URLField()
    username = models.CharField(max_length=64)

    panels = [
        FieldPanel("name"),
        FieldPanel("username"),
        FieldPanel("url"),
    ]

    def __str__(self) -> str:
        return self.name
