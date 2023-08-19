from django.apps import AppConfig
from health_check.plugins import plugin_dir


class CodeBlockAppConfig(AppConfig):
    name = "website.contrib.code_block"

    def ready(self) -> None:
        from .healthchecks import GitHubLinguistHealthCheckBackend

        plugin_dir.register(GitHubLinguistHealthCheckBackend)
