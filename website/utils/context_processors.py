from django.conf import settings
from django.http.request import HttpRequest


def global_vars(request: HttpRequest) -> dict:
    # noop caching in preview
    fragment_cache_ttl = 0 if getattr(request, "is_preview", False) else 3600
    return {
        "SEO_INDEX": settings.SEO_INDEX,
        "DEBUG": settings.DEBUG,
        "FRAGMENT_CACHE_TTL": fragment_cache_ttl,
        "FRAGMENT_CACHE_TTL_JITTER": fragment_cache_ttl * 0.1,
        "ACTIVITYPUB_HOST": settings.ACTIVITYPUB_HOST,
    }
