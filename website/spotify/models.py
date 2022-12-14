from datetime import timedelta
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

    content_panels = [
        panel
        for panel in BaseContentPage.content_panels
        if getattr(panel, "field_name", None) != "subtitle"
    ]

    settings_panels = BaseContentPage.settings_panels + [
        FieldPanel("spotify_playlist_id")
    ]

    search_fields = [
        panel
        for panel in BaseContentPage.search_fields
        if panel.field_name not in ["body", "subtitle"]
    ]

    @property
    def show_table_of_contents(self) -> bool:
        return False

    @cached_property
    def reading_time(self) -> timedelta:
        return timedelta(
            milliseconds=sum(
                track["track"]["duration_ms"] for track in self.playlist_data["tracks"]
            )
        )

    @cached_property
    def word_count(self) -> int:
        return 0

    @cached_property
    def subtitle(self) -> str:
        return self.playlist_data["description"]

    @cached_property
    def playlist_cache_key(self) -> str:
        return f"spotify_playlist_{self.spotify_playlist_id}"

    @cached_property
    def playlist_data(self) -> dict:
        playlist_data = cache.get(self.playlist_cache_key)

        if playlist_data is None:
            playlist_data = client.get_playlist(self.spotify_playlist_id)
            # Cache for 1 week
            cache.set(self.playlist_cache_key, playlist_data, 604800)

        return playlist_data

    def get_context(self, request: HttpRequest) -> dict:
        context = super().get_context(request)
        context["playlist"] = self.playlist_data
        return context
