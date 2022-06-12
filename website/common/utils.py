from typing import Type

from wagtail.models import Page
from wagtail.models import get_page_models as get_wagtail_page_models


def get_page_models() -> list[Type[Page]]:
    page_models = get_wagtail_page_models().copy()
    page_models.remove(Page)
    return page_models
