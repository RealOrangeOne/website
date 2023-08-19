from health_check.backends import BaseHealthCheckBackend

from .utils import _get_linguist_colours


class GitHubLinguistHealthCheckBackend(BaseHealthCheckBackend):
    def check_status(self) -> None:
        colours = _get_linguist_colours()

        if colours is None:
            self.add_error("No colours provided")

    def identifier(self) -> str:
        return "GitHub Linguist Colours"
