from django.urls import path

from . import views

app_name = "legacy"

urlpatterns = [
    path("posts/index.xml", views.PostsFeedView.as_view()),
    path("index.xml", views.AllPagesFeedView.as_view()),
    path("tags/<slug:slug>/", views.TagView.as_view()),
    path("tags/", views.TagView.as_view()),
    path("categories/", views.TagView.as_view()),
]
