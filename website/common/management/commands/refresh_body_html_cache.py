from django.core.cache import cache
from django.core.management.base import BaseCommand
from wagtail.models import Page

from website.common.models import BaseContentPage


class Command(BaseCommand):
    def handle(self, *args: list, **options: dict) -> None:
        for page in Page.objects.all().specific().iterator():
            if not isinstance(page, BaseContentPage):
                continue

            self.stdout.write(f"Refresh body cache: {page.title}")
            cache.delete(page.body_html_cache_key)
            page._body_html  # Prime cache
