from dataclasses import dataclass
from itertools import islice, pairwise
from typing import Type

from bs4 import BeautifulSoup, SoupStrainer
from django.conf import settings
from django.http.request import HttpRequest
from django.utils.text import slugify, smart_split
from more_itertools import ilen
from wagtail.models import Page
from wagtail.models import get_page_models as get_wagtail_page_models
from wagtail.query import PageQuerySet

HEADER_TAGS = ["h2", "h3", "h4", "h5", "h6"]


@dataclass
class TocEntry:
    title: str
    slug: str
    level: int
    children: list


def get_table_of_contents(html: str) -> list[TocEntry]:
    soup = BeautifulSoup(html, "lxml", parse_only=SoupStrainer(HEADER_TAGS))

    heading_levels = [
        TocEntry(tag.text, slugify(tag.text), int(tag.name[1]), []) for tag in soup
    ]

    # Abort if there are no headings
    if not heading_levels:
        return []

    # Ensure heading levels are sequential
    for heading, next_heading in pairwise(heading_levels):
        if next_heading.level - heading.level > 1:
            next_heading.level = heading.level + 1

    # Lower heading levels to 0
    min_level = min([h.level for h in heading_levels])
    for heading in heading_levels:
        heading.level -= min_level

    # A dummy root node, so we can pretend this is a tree
    root = TocEntry("", "", 0, [])

    # https://stackoverflow.com/a/44015834
    for heading in heading_levels:
        last = root
        for _ in range(heading.level):
            last = last.children[-1]
        last.children.append(heading)

    return root.children


def get_page_models() -> list[Type[Page]]:
    page_models = get_wagtail_page_models().copy()
    page_models.remove(Page)
    return page_models


def show_toolbar_callback(request: HttpRequest) -> bool:
    return settings.DEBUG


def count_words(text: str) -> int:
    """
    Count the number of words in the text, without duplicating the item in memory
    """
    return ilen(smart_split(text))


def extract_text(html: str) -> str:
    """
    Get the plain text of some HTML.
    """
    lines = (
        text.strip(" \n") for text in BeautifulSoup(html, "lxml").find_all(text=True)
    )
    return " ".join(line for line in lines if line)


def truncate_string(text: str, words: int) -> str:
    return " ".join(islice(smart_split(text), words))


def prefetch_for_listing(queryset: PageQuerySet) -> PageQuerySet:
    """
    Prefetch a queryset ready for listing.

    This should be a queryset method, but dealing with lots of
    different page models is a pain.
    """
    return queryset.select_related("hero_image", "hero_unsplash_photo")
