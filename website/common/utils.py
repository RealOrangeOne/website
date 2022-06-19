from typing import NamedTuple, Type

from django.conf import settings
from django.http.request import HttpRequest
from wagtail.models import Page
from wagtail.models import get_page_models as get_wagtail_page_models


class TocEntry(NamedTuple):
    title: str
    slug: str
    children: list


def get_table_of_contents() -> list[TocEntry]:
    return [
        TocEntry(
            "Title 1",
            "title-1",
            [
                TocEntry("Title 1.1", "title-11", []),
                TocEntry("Title 1.2", "title-12", []),
                TocEntry("Title 1.3", "title-13", []),
            ],
        ),
        TocEntry("Title 2", "title-2", []),
        TocEntry("Title 3", "title-3", []),
    ]


def get_page_models() -> list[Type[Page]]:
    page_models = get_wagtail_page_models().copy()
    page_models.remove(Page)
    return page_models


def show_toolbar_callback(request: HttpRequest) -> bool:
    return settings.DEBUG
