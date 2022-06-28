from django.http import Http404, HttpRequest, HttpResponse
from django.views.decorators.cache import cache_control
from django.views.decorators.http import etag
from pygments.formatters.html import HtmlFormatter
from pygments.util import ClassNotFound

from .utils import PYGMENTS_VERSION


def pygments_etag(request: HttpRequest, name: str) -> str:
    return PYGMENTS_VERSION


@etag(pygments_etag)
@cache_control(max_age=3600, public=True)
def pygments_styles(request: HttpRequest, name: str) -> HttpResponse:
    try:
        formatter = HtmlFormatter(style=name)
    except ClassNotFound:
        # Raising an exception here bypasses the cache header
        raise Http404
    return HttpResponse(
        formatter.get_style_defs("." + formatter.cssclass), content_type="text/css"
    )
