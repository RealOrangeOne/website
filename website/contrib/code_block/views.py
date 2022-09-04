from django.http import HttpRequest, HttpResponse
from django.utils.datastructures import OrderedSet
from django.views.decorators.cache import cache_control
from pygments.formatters.html import HtmlFormatter


@cache_control(max_age=3600)
def pygments_styles(request: HttpRequest) -> HttpResponse:
    default_styles = (
        HtmlFormatter(style="default")
        .get_style_defs("html:not(.dark-mode) .highlight")
        .split("\n")
    )
    dark_styles = (
        HtmlFormatter(style="monokai")
        .get_style_defs("html.dark-mode .highlight")
        .split("\n")
    )
    return HttpResponse(
        "".join(OrderedSet(default_styles + dark_styles)), content_type="text/css"
    )
