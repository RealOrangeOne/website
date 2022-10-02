from argparse import ArgumentParser

from django.core.cache import DEFAULT_CACHE_ALIAS, caches
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def add_arguments(self, parser: ArgumentParser) -> None:
        parser.add_argument(
            "cache",
            type=str,
            default=DEFAULT_CACHE_ALIAS,
            nargs="?",
            choices=list(caches),
            help="Cache alias. Default: %(default)s",
        )

    def handle(self, *args: list, **options: dict) -> None:
        cache_alias = options["cache"]
        self.stdout.write(f"Purging cache {cache_alias}")
        caches[cache_alias].clear()
