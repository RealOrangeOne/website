import requests
from django.conf import settings
from health_check.backends import BaseHealthCheckBackend


class UnsplashHealthCheckBackend(BaseHealthCheckBackend):
    def check_status(self) -> None:
        try:
            requests.get(
                "https://api.unsplash.com/me",
                headers={
                    "Accept-Version": "v1",
                    "Authorization": f"Client-ID {settings.UNSPLASH_CLIENT_ID}",
                },
            ).raise_for_status()
        except Exception as e:
            self.add_error(str(e))

    def identifier(self) -> str:
        return "Unsplash API"
