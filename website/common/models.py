from django.db import models

from wagtail.models import Page


class BasePage(Page):
    class Meta:
        abstract = True

    @property
    def body_class(self):
        return "page-" + self._meta.db_table.replace("_", "-")
