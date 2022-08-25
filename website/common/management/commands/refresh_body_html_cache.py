from django.core.cache import cache
from django.core.management.base import BaseCommand
from wagtail.models import Page

from website.common.models import BaseContentPage
from website.utils.queue import enqueue_or_sync


def refresh_cache(page_id: int) -> None:
    page = Page.objects.get(id=page_id).specific
    cache.delete(page.body_html_cache_key)
    page._body_html  # Prime cache


class Command(BaseCommand):
    def handle(self, *args: list, **options: dict) -> None:
        for page in Page.objects.all().specific().only("id", "title").iterator():
            if not isinstance(page, BaseContentPage):
                continue

            enqueue_or_sync(refresh_cache, args=[page.id])
