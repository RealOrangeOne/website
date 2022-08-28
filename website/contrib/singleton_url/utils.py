from typing import Type

from django.core.cache import cache
from django.http.request import HttpRequest
from wagtail.models import Page


class SingletonURLCache:
    @classmethod
    def get_url_cache_key(cls, model: Type[Page]) -> str:
        return f"singleton_url_{model.__name__}"

    @classmethod
    def get_url(
        cls, model: Type[Page], request: HttpRequest | None = None
    ) -> str | None:
        cache_key = cls.get_url_cache_key(model)

        url = cache.get(cache_key)

        if url is None:
            # `.first` is marginally more efficient than `.get`
            page = Page.objects.type(model).first()

            if page is None:
                return None

            url = page.get_full_url(request)

            cache.set(cache_key, url, 86400)

        return url
