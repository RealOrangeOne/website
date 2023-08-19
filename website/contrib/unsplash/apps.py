from django.apps import AppConfig
from health_check.plugins import plugin_dir


class UnsplashAppConfig(AppConfig):
    name = "website.contrib.unsplash"

    def ready(self) -> None:
        from .healthchecks import UnsplashHealthCheckBackend

        plugin_dir.register(UnsplashHealthCheckBackend)
