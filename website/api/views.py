from django.http.request import HttpRequest
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from wagtail.models import Page
from wagtail.query import PageQuerySet

from . import serializers


class PingAPIView(APIView):
    """
    PONGs
    """

    def get(self, request: HttpRequest) -> Response:
        return Response("PONG")


class PageLinksAPIView(ListAPIView):
    serializer_class = serializers.PageLinkSerializer

    def get_queryset(self) -> PageQuerySet:
        return (
            Page.objects.live()
            .exclude(depth__lte=1)
            .only("id", "url_path", "title")
            .order_by("title")
        )
