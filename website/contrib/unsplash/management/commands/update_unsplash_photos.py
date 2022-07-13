from argparse import ArgumentParser
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from website.contrib.unsplash.models import UnsplashPhoto
from website.contrib.unsplash.utils import get_unsplash_photo
from website.utils.queue import enqueue_or_sync


def update_photo(photo: UnsplashPhoto) -> None:
    photo.data = get_unsplash_photo(photo.unsplash_id)
    photo.data_last_updated = timezone.now()
    photo.save()


class Command(BaseCommand):
    def add_arguments(self, parser: ArgumentParser) -> None:
        parser.add_argument("--max-age-days", type=int, default=10)

    def handle(self, *args: list, **options: dict) -> None:
        max_age_days: int = options["max_age_days"]  # type: ignore
        max_age = timezone.now() - timedelta(days=max_age_days)
        photos = UnsplashPhoto.objects.filter(data_last_updated__lte=max_age)
        self.stdout.write(f"Found {photos.count()} photos to update.")

        for photo in photos:
            self.stdout.write(f"Updating {photo.unsplash_id}")
            enqueue_or_sync(update_photo, args=[photo])
