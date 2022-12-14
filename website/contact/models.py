from django.core.validators import RegexValidator
from django.db import models
from django.http.request import HttpRequest
from django.utils.functional import cached_property
from django.utils.text import slugify
from wagtail.admin.panels import FieldPanel
from wagtail.search import index
from wagtail.snippets.models import register_snippet

from website.common.models import BaseContentPage
from website.common.utils import TocEntry


@register_snippet
class OnlineAccount(models.Model, index.Indexed):
    name = models.CharField(max_length=64, unique=True)
    url = models.URLField()
    username = models.CharField(max_length=64)
    icon = models.CharField(
        max_length=64, blank=True, validators=[RegexValidator(r"[a-z-\\s]")]
    )

    panels = [
        FieldPanel("name"),
        FieldPanel("icon"),
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


class ContactPage(BaseContentPage):
    max_count = 1
    subpage_types: list = []

    @cached_property
    def show_reading_time(self) -> bool:
        return False

    @cached_property
    def online_accounts(self) -> models.QuerySet:
        return OnlineAccount.objects.all().order_by("name")

    @cached_property
    def table_of_contents(self) -> list[TocEntry]:
        return [
            TocEntry(account.name, account.slug, 0, [])
            for account in self.online_accounts
        ]

    def get_context(self, request: HttpRequest) -> dict:
        context = super().get_context(request)
        context["accounts"] = self.online_accounts
        return context
