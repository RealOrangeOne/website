from django.apps import AppConfig
from health_check.plugins import plugin_dir


class SpotifyAppConfig(AppConfig):
    name = "website.spotify"

    def ready(self) -> None:
        from .healthchecks import SpotifyHealthCheckBackend

        plugin_dir.register(SpotifyHealthCheckBackend)
