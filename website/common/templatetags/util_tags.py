from django.template import Library
from wagtail.models import Page

register = Library()


@register.filter(name="range")
def do_range(stop: int) -> range:
    return range(stop)


@register.simple_tag(takes_context=True)
def pagefullurl(context: dict, page: Page) -> str:
    return page.get_full_url(context["request"])
