import requests
from django.conf import settings
from health_check.backends import BaseHealthCheckBackend


class SpotifyHealthCheckBackend(BaseHealthCheckBackend):
    def check_status(self) -> None:
        requests.get(
            f"https://{settings.SPOTIFY_PROXY_HOST}/.health/"
        ).raise_for_status()

    def identifier(self) -> str:
        return "Spotify Proxy"
