from django.urls import include, path
from rest_framework import permissions
from rest_framework.schemas import get_schema_view

from . import views

app_name = "api"

api_urlpatterns = [
    path("ping", views.PingAPIView.as_view(), name="ping"),
    path("page-links", views.PageLinksAPIView.as_view(), name="page-links"),
    path("lmotfy", views.LMOTFYAPIView.as_view(), name="lmotfy"),
]

schema_view = get_schema_view(
    title="Website API",
    version="v1",
    description="Random API endpoints for cool things",
    public=True,
    permission_classes=[permissions.AllowAny],
    patterns=[
        # HACK: Ensure the created URLs are fully-formed
        path("api/", include(api_urlpatterns))
    ],
)

urlpatterns = [
    path(
        "schema/",
        schema_view,
        name="schema",
    ),
    path("", views.SwaggerRedirectView.as_view(), name="index"),
] + api_urlpatterns
