from dataclasses import dataclass
from itertools import pairwise
from typing import Any, Optional, Type
from urllib.parse import urlsplit, urlunsplit

import requests
from bs4 import BeautifulSoup, SoupStrainer
from django.conf import settings
from django.db import models
from django.http import QueryDict
from django.http.request import HttpRequest
from django.utils.text import slugify
from django_cache_decorator import django_cache_decorator
from metadata_parser import MetadataParser, ParsedResult
from wagtail.models import Page, Site
from wagtail.models import get_page_models as get_wagtail_page_models

HEADER_TAGS = ["h2", "h3", "h4", "h5", "h6"]

requests_session = requests.Session()


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


def extract_text(html: str) -> str:
    """
    Get the plain text of some HTML.
    """
    return (
        BeautifulSoup(html.replace("<p", " <p"), "lxml").get_text().replace("\n", " ")
    )


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
        return requests_session.head(url).headers.get("Content-Type")
    except requests.exceptions.RequestException:
        return None


def get_or_none(queryset: models.QuerySet) -> models.Model:
    """
    Helper method to get a single instance, or None if there is not exactly 1 matches
    """
    try:
        return queryset.get()
    except (queryset.model.DoesNotExist, queryset.model.MultipleObjectsReturned):
        return None


@django_cache_decorator(time=21600)
def get_ai_robots_txt() -> str:
    """
    https://github.com/ai-robots-txt/ai.robots.txt
    """
    return requests_session.get(
        "https://raw.githubusercontent.com/ai-robots-txt/ai.robots.txt/main/robots.txt"
    ).content.decode()


@django_cache_decorator(time=21600)
def get_page_metadata(url: str) -> ParsedResult:
    metadata = MetadataParser(url=url, search_head_only=True).parsed_result

    # HACK: BeautifulSoup doesn't pickle nicely, and so can't be cached
    metadata.soup = None

    return metadata


def extend_query_params(url: str, params: dict[str, Any]) -> str:
    scheme, netloc, path, query, fragment = urlsplit(url)
    query_dict = QueryDict(query, mutable=True)

    for k, v in params.items():
        if v is None:
            del query_dict[k]
        else:
            query_dict[k] = v

    return urlunsplit((scheme, netloc, path, query_dict.urlencode(), fragment))
