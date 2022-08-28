from django.template import Library

from website.contrib.singleton_page.utils import SingletonPageCache
from website.home.models import HomePage

register = Library()


@register.inclusion_tag("common/footer.html")
def footer() -> dict:
    return {
        "homepage_url": SingletonPageCache.get_url(HomePage),
    }
