import requests
from django.conf import settings


def is_valid_playlist(playlist_id: str) -> bool:
    return requests.get(
        f"https://{settings.SPOTIFY_PROXY_HOST}/v1/playlists/{playlist_id}"
    ).ok


def get_playlist(playlist_id: str) -> dict:
    response = requests.get(
        f"https://{settings.SPOTIFY_PROXY_HOST}/v1/playlists/{playlist_id}"
    )
    response.raise_for_status()
    return response.json()
