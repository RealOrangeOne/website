from functools import cache
from importlib.metadata import version

import yaml
from django_cache_decorator import django_cache_decorator

from website.common.utils import requests_session

PYGMENTS_VERSION = version("pygments")
PYGMENTS_VERSION_SLUG = PYGMENTS_VERSION.replace(".", "-")

LINGUIST_DATA_URL = "https://raw.githubusercontent.com/github/linguist/master/lib/linguist/languages.yml"


@django_cache_decorator(time=600)
def _get_linguist_colours() -> dict[str, str]:
    response = requests_session.get(LINGUIST_DATA_URL)

    response.raise_for_status()

    linguist_data = yaml.safe_load(response.text)

    return {
        language.lower(): data["color"]
        for language, data in linguist_data.items()
        if data.get("color")
    }


@cache
@django_cache_decorator(time=21600)
def get_linguist_colours() -> dict[str, str]:
    return _get_linguist_colours()
