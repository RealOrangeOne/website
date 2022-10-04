from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key
from django.http.request import HttpRequest
from wagtail import hooks
from wagtail.models import Page

from website.common.models import BasePage

FRAGMENT_CACHES = {"listing-item", "content-details"}


@hooks.register("after_edit_page")
def clear_fragment_cache(request: HttpRequest, page: Page) -> None:
    if not isinstance(page, BasePage):
        return

    cache.delete_many(
        [
            # Empty string is for the empty value of `request.is_preview`
            make_template_fragment_key(cache_name, [page.id, False])
            for cache_name in FRAGMENT_CACHES
        ]
    )
