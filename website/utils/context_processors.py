from django.conf import settings
from django.http.request import HttpRequest


def global_vars(request: HttpRequest) -> dict:
    return {"SEO_INDEX": settings.SEO_INDEX, "DEBUG": settings.DEBUG}
