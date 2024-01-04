from django.urls import path

from . import views

urlpatterns = [
    path("opensearch.xml", views.OpenSearchView.as_view(), name="opensearch"),
    path(
        "opensearch-suggestions/",
        views.OpenSearchSuggestionsView.as_view(),
        name="opensearch-suggestions",
    ),
]
