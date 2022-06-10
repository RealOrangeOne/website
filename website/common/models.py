from django.db import models

from wagtail.models import Page


class BasePage(Page):
    class Meta:
        abstract = True
