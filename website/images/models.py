from django.db import models
from wagtail.images.models import AbstractImage, AbstractRendition


class CustomImage(AbstractImage):
    pass


class CustomRendition(AbstractRendition):
    image = models.ForeignKey(
        CustomImage, on_delete=models.CASCADE, related_name="renditions"
    )

    class Meta:
        unique_together = (("image", "filter_spec", "focal_point_key"),)
