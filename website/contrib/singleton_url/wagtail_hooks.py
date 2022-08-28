from django.core.cache import cache
from wagtail import hooks

from website.common.utils import get_page_models

from .utils import SingletonURLCache


@hooks.register("after_move_page")
def clear_singleton_url_cache(**kwargs: dict) -> None:
    """
    Clear all page caches, in case a parent has moved
    """
    cache.delete_many(
        [SingletonURLCache.get_url_cache_key(model) for model in get_page_models()]
    )
