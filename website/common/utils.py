from dataclasses import dataclass
from itertools import pairwise
from typing import Type

from bs4 import BeautifulSoup
from django.conf import settings
from django.http.request import HttpRequest
from django.utils.text import slugify
from wagtail.models import Page
from wagtail.models import get_page_models as get_wagtail_page_models

HEADER_TAGS = ["h2", "h3", "h4", "h5", "h6"]


@dataclass
class TocEntry:
    title: str
    slug: str
    level: int
    children: list


def get_table_of_contents(html: str) -> list[TocEntry]:
    soup = BeautifulSoup(html, "lxml")

    headings = soup.find_all(HEADER_TAGS)

    heading_levels = [
        TocEntry(tag.text, slugify(tag.text), int(tag.name[1]), []) for tag in headings
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


def add_heading_anchors(html: str) -> str:
    soup = BeautifulSoup(html, "lxml")
    for tag in soup.find_all(HEADER_TAGS):
        slug = slugify(tag.text)
        anchor = soup.new_tag("a", href="#" + slug, id=slug)
        anchor.string = "#"
        anchor.attrs["class"] = "heading-anchor"
        tag.insert(0, anchor)
    return str(soup)


def get_page_models() -> list[Type[Page]]:
    page_models = get_wagtail_page_models().copy()
    page_models.remove(Page)
    return page_models


def show_toolbar_callback(request: HttpRequest) -> bool:
    return settings.DEBUG
