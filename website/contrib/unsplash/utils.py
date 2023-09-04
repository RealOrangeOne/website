from django.conf import settings

from website.common.utils import requests_session


def get_unsplash_photo(image_id: str) -> dict:
    response = requests_session.get(
        f"https://api.unsplash.com/photos/{image_id}",
        headers={
            "Accept-Version": "v1",
            "Authorization": f"Client-ID {settings.UNSPLASH_CLIENT_ID}",
        },
    )

    if response.status_code == 404:
        raise ValueError(f"Unknown image {image_id}")

    response.raise_for_status()

    return response.json()
