from argparse import ArgumentParser

from django.core.cache import DEFAULT_CACHE_ALIAS, caches
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def add_arguments(self, parser: ArgumentParser) -> None:
        parser.add_argument(
            "cache",
            type=str,
            default=DEFAULT_CACHE_ALIAS,
            choices=sorted(list(caches)),
            help="Cache to clear",
        )

    def handle(self, *args: list, **options: dict) -> None:
        cache_name: str = options["cache"]  # type: ignore
        caches[cache_name].clear()
        self.stdout.write(f"Cleared cache '{cache_name}'.")
