from django.conf import settings

from website.common.utils import requests_session

API_LIMIT = 50


def is_valid_playlist(playlist_id: str) -> bool:
    return requests_session.get(
        f"https://{settings.SPOTIFY_PROXY_HOST}/v1/playlists/{playlist_id}"
    ).ok


def get_playlist(playlist_id: str) -> dict:
    playlist_response = requests_session.get(
        f"https://{settings.SPOTIFY_PROXY_HOST}/v1/playlists/{playlist_id}",
        params={"fields": "name,external_urls.spotify,tracks.total,description"},
    )
    playlist_response.raise_for_status()
    playlist_data = playlist_response.json()

    tracks = []
    for offset in range(0, playlist_data["tracks"]["total"], API_LIMIT):
        tracks_response = requests_session.get(
            f"https://{settings.SPOTIFY_PROXY_HOST}/v1/playlists/{playlist_id}/tracks",
            params={
                "offset": str(offset),
                "limit": str(API_LIMIT),
                "fields": "items(track(name,album.name,album.images,artists.name,external_urls.spotify,preview_url,duration_ms))",
            },
        )
        tracks_response.raise_for_status()
        tracks.extend(tracks_response.json()["items"])

    playlist_data["tracks"] = sorted(
        tracks, key=lambda track: track["track"]["name"].lower()
    )

    return playlist_data
