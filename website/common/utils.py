from typing import Type

from django.conf import settings
from django.http.request import HttpRequest
from wagtail.models import Page
from wagtail.models import get_page_models as get_wagtail_page_models


def get_page_models() -> list[Type[Page]]:
    page_models = get_wagtail_page_models().copy()
    page_models.remove(Page)
    return page_models


def show_toolbar_callback(request: HttpRequest) -> bool:
    return settings.DEBUG
