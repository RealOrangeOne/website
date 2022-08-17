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

    def get_context(self, request: HttpRequest) -> dict:
        context = super().get_context(request)
        context["playlist"] = client.get_playlist(self.spotify_playlist_id)
        return context
