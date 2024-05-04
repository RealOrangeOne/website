from django.core.cache import cache
from wagtail import hooks
from wagtail.models import Page

from website.common.utils import get_page_models

from .utils import SingletonPageCache


@hooks.register("after_move_page")
def clear_singleton_url_cache(page_to_move: Page) -> None:
    """
    Clear all page caches, in case a parent has moved
    """
    cache.delete_many(
        [SingletonPageCache.get_url_cache_key(model) for model in get_page_models()]
    )
