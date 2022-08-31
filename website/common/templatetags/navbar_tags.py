from django.template import Library

from website.contrib.singleton_page.utils import SingletonPageCache
from website.home.models import HomePage
from website.search.models import SearchPage

register = Library()


@register.inclusion_tag("common/navbar.html", takes_context=True)
def navbar(context: dict) -> dict:
    request = context["request"]
    homepage = HomePage.objects.get()
    return {
        "homepage_url": SingletonPageCache.get_url(HomePage, request),
        "nav_pages": homepage.get_children()
        .live()
        .public()
        .filter(show_in_menus=True)
        .order_by("title"),
        "search_page_url": SingletonPageCache.get_url(SearchPage, request),
    }
