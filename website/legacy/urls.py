from django.urls import path

from . import views

app_name = "legacy"

urlpatterns = [
    path("posts/index.xml", views.PostsFeedView.as_view()),
    path("index.xml", views.AllPagesFeedView.as_view()),
]
