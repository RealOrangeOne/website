from dataclasses import dataclass
from itertools import islice, pairwise
from typing import Iterable, Optional, Type

import requests
from bs4 import BeautifulSoup, SoupStrainer
from django.conf import settings
from django.http.request import HttpRequest
from django.utils.text import re_words, slugify
from django_cache_decorator import django_cache_decorator
from wagtail.models import Page, Site
from wagtail.models import get_page_models as get_wagtail_page_models

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
        TocEntry(tag.text, heading_id(tag.text), int(tag.name[1]), []) for tag in soup
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


def split_words(text: str) -> Iterable[str]:
    for word in re_words.split(text):
        if word and word.strip():
            yield word.strip()


def count_words(text: str) -> int:
    """
    Count the number of words in the text, without duplicating the item in memory
    """
    return len(list(split_words(text)))


def extract_text(html: str) -> str:
    """
    Get the plain text of some HTML.
    """
    return (
        BeautifulSoup(html.replace("<p", " <p"), "lxml").get_text().replace("\n", " ")
    )


def truncate_string(text: str, words: int) -> str:
    return " ".join(islice(split_words(text), words))


def heading_id(heading: str) -> str:
    """
    Convert a heading into an identifier which is valid for a HTML id attribute
    """
    if not heading:
        return ""

    slug = slugify(heading)
    if slug[0].isdigit():
        return "ref-" + slug
    return slug


@django_cache_decorator(time=300)
def get_site_title() -> str:
    return Site.objects.values_list("site_name", flat=True).first()


@django_cache_decorator(time=21600)
def get_url_mime_type(url: str) -> Optional[str]:
    try:
        return requests.head(url).headers.get("Content-Type")
    except requests.exceptions.RequestException:
        return None
