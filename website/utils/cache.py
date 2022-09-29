import inspect
from functools import wraps
from typing import Callable, Type, TypeVar

from django.core.cache import cache
from django.db.models import Model
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.functional import cached_property

T = TypeVar("T")


def get_cache_key(instance: Model, method: Callable) -> str:
    return f"page_{method.__name__}_{instance.pk}"


def get_cached_model_properties(model: Type[Model]) -> list[str]:
    return [
        name
        for name, _ in inspect.getmembers(
            model, predicate=lambda p: hasattr(p, "__cached__")
        )
    ]


def cached_model_property(f: Callable[[Model], T]) -> T:
    @cached_property
    @wraps(f)
    def wrapped(self: Model) -> T:
        cache_key = get_cache_key(self, f)
        value = cache.get(cache_key)

        if value is None:
            value = f(self)
            # Cache for 1 week
            cache.set(cache_key, value, 604800)

        return value

    wrapped.__cached__ = True
    return wrapped


@receiver(post_save)
def clear_cached_model_properties(
    sender: Type, instance: Model, **kwargs: dict
) -> None:
    cached_model_properties = get_cached_model_properties(instance.__class__)

    if cached_model_properties:
        cache.delete_many(
            [
                get_cache_key(instance, getattr(instance.__class__, name).real_func)
                for name in cached_model_properties
            ]
        )

        # Prime caches again
        for name in cached_model_properties:
            getattr(instance, name)
