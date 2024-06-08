from django.core.cache import cache
from django.core.management.base import BaseCommand
from django_tasks import task

from website.spotify.models import SpotifyPlaylistPage


@task()
def refresh_cache(page_id: int) -> None:
    page = SpotifyPlaylistPage.objects.get(id=page_id)
    cache.delete(page.playlist_cache_key)

    # Prime cache
    page.playlist_data  # noqa: B018


class Command(BaseCommand):
    def handle(self, *args: list, **options: dict) -> None:
        for page_id in (
            SpotifyPlaylistPage.objects.all().values_list("id", flat=True).iterator()
        ):
            refresh_cache.enqueue(page_id)
