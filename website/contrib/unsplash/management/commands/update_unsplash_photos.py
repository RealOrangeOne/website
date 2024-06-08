from argparse import ArgumentParser
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone
from django_tasks import task

from website.contrib.unsplash.models import UnsplashPhoto
from website.contrib.unsplash.utils import get_unsplash_photo


@task()
def update_photo(photo_id: int) -> None:
    photo = UnsplashPhoto.objects.get(id=photo_id)
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

        for photo_id, unsplash_id in photos.values_list("id", "unsplash_id"):
            self.stdout.write(f"Updating {unsplash_id}")
            update_photo.enqueue(photo_id)
