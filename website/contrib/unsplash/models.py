from django.db import models


class UnsplashPhoto(models.Model):
    unsplash_id = models.CharField(unique=True, max_length=11, db_index=True)
    data = models.JSONField()

    def get_description(self) -> str:
        return self.data["description"]

    def get_hero_image_url(self) -> str:
        return self.data["urls"]["regular"]

    def get_thumbnail_url(self) -> str:
        return self.data["urls"]["thumb"]
