from django.conf import settings
from health_check.backends import BaseHealthCheckBackend

from website.common.utils import requests_session


class SpotifyHealthCheckBackend(BaseHealthCheckBackend):
    def check_status(self) -> None:
        try:
            requests_session.get(
                f"https://{settings.SPOTIFY_PROXY_HOST}/.health/"
            ).raise_for_status()
        except Exception as e:
            self.add_error(str(e))

    def identifier(self) -> str:
        return "Spotify Proxy"
