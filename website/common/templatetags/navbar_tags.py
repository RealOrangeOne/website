from django.template import Library
from wagtail.models import Page

from website.home.models import HomePage

register = Library()


@register.inclusion_tag("common/navbar.html")
def navbar(current_page: Page) -> dict:
    homepage = HomePage.objects.live().get()
    return {
        "current_page": current_page,
        "homepage": homepage,
        "nav_pages": homepage.get_children()
        .live()
        .filter(show_in_menus=True)
        .order_by("title"),
    }
