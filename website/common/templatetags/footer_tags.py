from django.template import Library

from website.contrib.singleton_url.utils import SingletonURLCache
from website.home.models import HomePage

register = Library()


@register.inclusion_tag("common/footer.html")
def footer() -> dict:
    return {
        "homepage_url": SingletonURLCache.get_url(HomePage),
    }
