from django.urls import include, path, re_path
from django.views.generic import RedirectView
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from . import views

app_name = "api"

api_urlpatterns = [
    path("ping", views.PingAPIView.as_view(), name="ping"),
    path("page-links", views.PageLinksAPIView.as_view(), name="page-links"),
    path("lmotfy", views.LMOTFYAPIView.as_view(), name="lmotfy"),
]

schema_view = get_schema_view(
    openapi.Info(
        title="Website API",
        default_version="v1",
        description="Random API endpoints for cool things",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
    patterns=[
        # HACK: Ensure the created URLs are fully-formed
        path("api/", include(api_urlpatterns))
    ],
)

urlpatterns = [
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=60 * 60),
        name="schema-json",
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=60 * 60),
        name="schema-swagger-ui",
    ),
    path("", RedirectView.as_view(pattern_name="api:schema-swagger-ui")),
] + api_urlpatterns
