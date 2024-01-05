from django.template import Library
from django.utils.encoding import force_str
from wagtail.models import Page
from wagtail.rich_text import RichText

from website.common import utils

register = Library()


@register.filter(name="range")
def do_range(stop: int) -> range:
    return range(stop)


@register.simple_tag(takes_context=True)
def pagefullurl(context: dict, page: Page) -> str:
    return page.get_full_url(context["request"])


@register.filter()
def extract_text(html: str | RichText) -> str:
    return utils.extract_text(force_str(html))
