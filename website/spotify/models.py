from functools import cached_property

from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.db import models
from django.http.request import HttpRequest
from wagtail.admin.panels import FieldPanel

from website.common.models import BaseContentPage

from . import client


def validate_playlist_id(playlist_id: str) -> None:
    if not client.is_valid_playlist(playlist_id):
        raise ValidationError("Unknown playlist id")


class SpotifyPlaylistPage(BaseContentPage):
    subpage_types: list = []

    spotify_playlist_id = models.CharField(
        max_length=32, unique=True, validators=[validate_playlist_id]
    )

    content_panels = BaseContentPage.content_panels + [
        FieldPanel("spotify_playlist_id")
    ]

    @property
    def table_of_contents(self) -> list:
        return []

    @property
    def reading_time(self) -> int:
        return 0

    @cached_property
    def playlist_cache_key(self) -> str:
        return f"spotify_playlist_{self.spotify_playlist_id}"

    def get_playlist_data(self) -> dict:
        playlist_data = cache.get(self.playlist_cache_key)

        if playlist_data is None:
            playlist_data = client.get_playlist(self.spotify_playlist_id)
            # Cache for 1 week
            cache.set(self.playlist_cache_key, playlist_data, 604800)

        return playlist_data

    def get_context(self, request: HttpRequest) -> dict:
        context = super().get_context(request)
        context["playlist"] = self.get_playlist_data()
        return context
