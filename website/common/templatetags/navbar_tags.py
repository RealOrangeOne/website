from django.template import Library

from website.home.models import HomePage

register = Library()


@register.inclusion_tag("common/navbar.html")
def navbar() -> dict:
    homepage = HomePage.objects.live().get()
    return {
        "homepage": homepage,
        "nav_pages": homepage.get_children()
        .live()
        .filter(show_in_menus=True)
        .order_by("title"),
    }
