from django.urls import path

from . import views

app_name = "well-known"

urlpatterns = [
    path(
        "security.txt",
        views.SecurityView.as_view(),
        name="security-txt",
    ),
    path(
        "matrix/server",
        views.MatrixServerView.as_view(),
        name="matrix-server",
    ),
    path(
        "matrix/client",
        views.MatrixClientView.as_view(),
        name="matrix-client",
    ),
]
