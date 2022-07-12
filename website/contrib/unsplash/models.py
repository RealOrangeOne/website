from django.db import models


class UnsplashPhoto(models.Model):
    unsplash_id = models.CharField(unique=True, max_length=11, db_index=True)
    data = models.JSONField()
