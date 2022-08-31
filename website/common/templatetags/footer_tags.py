from django.template import Library

from website.contrib.singleton_page.utils import SingletonPageCache
from website.home.models import HomePage

register = Library()


@register.inclusion_tag("common/footer.html", takes_context=True)
def footer(context: dict) -> dict:
    request = context["request"]
    return {
        "homepage_url": SingletonPageCache.get_url(HomePage, request),
    }
