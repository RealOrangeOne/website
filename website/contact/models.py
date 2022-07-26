from django.db import models
from django.http.request import HttpRequest
from django.utils.functional import cached_property
from django.utils.text import slugify
from wagtail.admin.panels import FieldPanel
from wagtail.search import index
from wagtail.snippets.models import register_snippet

from website.common.models import BaseContentMixin, BasePage
from website.common.utils import TocEntry


@register_snippet
class OnlineAccount(models.Model, index.Indexed):
    name = models.CharField(max_length=64, unique=True)
    url = models.URLField()
    username = models.CharField(max_length=64)

    panels = [
        FieldPanel("name"),
        FieldPanel("username"),
        FieldPanel("url"),
    ]

    search_fields = [
        index.AutocompleteField("name"),
        index.FilterField("username"),
        index.SearchField("url"),
    ]

    def __str__(self) -> str:
        return self.name

    @cached_property
    def slug(self) -> str:
        return slugify(self.name)


class ContactPage(BaseContentMixin, BasePage):  # type: ignore[misc]
    max_count = 1
    subpage_types: list = []
    content_panels = BasePage.content_panels + BaseContentMixin.content_panels

    @cached_property
    def reading_time(self) -> int:
        """
        How does one read a list page?
        """
        return 0

    @cached_property
    def table_of_contents(self) -> list[TocEntry]:
        return [
            TocEntry(account.name, account.slug, 0, [])
            for account in OnlineAccount.objects.all().order_by("name")
        ]

    def get_context(self, request: HttpRequest) -> dict:
        context = super().get_context(request)
        context["accounts"] = OnlineAccount.objects.all().order_by("name")
        return context
