from django.apps import apps
from django.core.cache import cache
from django.core.management.base import BaseCommand

from website.utils.cache import get_cache_key, get_cached_model_properties
from website.utils.queue import enqueue_or_sync


def refresh_cache(
    app_label: str, model_name: str, model_id: int, cached_model_properties: list[str]
) -> None:
    Model = apps.get_model(app_label, model_name)
    instance = Model.objects.get(id=model_id)
    cache.delete_many(
        [
            get_cache_key(instance, getattr(instance.__class__, name).real_func)
            for name in cached_model_properties
        ]
    )

    # Prime caches again
    for name in cached_model_properties:
        getattr(instance, name)


class Command(BaseCommand):
    def handle(self, *args: list, **options: dict) -> None:
        for Model in apps.get_models():
            cached_model_properties = get_cached_model_properties(Model)

            if not cached_model_properties:
                continue
            for instance_id in (
                Model.objects.all().values_list("id", flat=True).iterator()
            ):
                enqueue_or_sync(
                    refresh_cache,
                    [
                        Model._meta.app_label,
                        Model._meta.model_name,
                        instance_id,
                        cached_model_properties,
                    ],
                )
