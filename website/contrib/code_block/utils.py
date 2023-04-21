from importlib.metadata import version

import requests
import yaml
from django_cache_decorator import django_cache_decorator

PYGMENTS_VERSION = version("pygments")
PYGMENTS_VERSION_SLUG = PYGMENTS_VERSION.replace(".", "-")

LINGUIST_DATA_URL = "https://raw.githubusercontent.com/github/linguist/master/lib/linguist/languages.yml"


@django_cache_decorator(time=21600)
def get_linguist_colours() -> dict[str, str]:
    response = requests.get(LINGUIST_DATA_URL)

    response.raise_for_status()

    linguist_data = yaml.safe_load(response.text)

    return {
        language.lower(): l["color"]
        for language, l in linguist_data.items()
        if l.get("color")
    }
