from typing import TypedDict

from django.db import models
from django.utils import timezone


class ImageURLs(TypedDict):
    raw: str
    full: str
    regular: str
    small: str
    thumb: str


class UnsplashPhoto(models.Model):
    unsplash_id = models.CharField(unique=True, max_length=11, db_index=True)
    data = models.JSONField()
    created = models.DateTimeField(auto_now_add=True)
    data_last_updated = models.DateTimeField(default=timezone.now)

    def get_description(self) -> str:
        return self.data["description"]

    def get_image_urls(self) -> ImageURLs:
        return self.data["urls"]

    def get_thumbnail_url(self) -> str:
        return self.get_image_urls()["thumb"]
