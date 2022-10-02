from django.core.cache import cache
from django.core.management.base import BaseCommand

from website.spotify.models import SpotifyPlaylistPage
from website.utils.queue import enqueue_or_sync


def refresh_cache(page_id: int) -> None:
    page = SpotifyPlaylistPage.objects.get(id=page_id)
    cache.delete(page.playlist_cache_key)
    page.playlist_data  # Prime cache


class Command(BaseCommand):
    def handle(self, *args: list, **options: dict) -> None:
        for page in SpotifyPlaylistPage.objects.all().defer_streamfields().iterator():
            enqueue_or_sync(refresh_cache, args=[page.id])
