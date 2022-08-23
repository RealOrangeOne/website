from django.http.request import HttpRequest
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from wagtail.models import Page
from wagtail.query import PageQuerySet

from website.blog.models import BlogPostListPage

from . import filters, serializers
from .pagination import CustomPageNumberPagination


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


class LMOTFYAPIView(ListAPIView):
    """
    Let Me Orange That For You
    """

    filter_backends = [filters.WagtailSearchFilter, OrderingFilter]
    serializer_class = serializers.LMOTFYSerializer
    ordering_fields = ["title", "date", "relevance"]
    ordering = ["relevance"]
    pagination_class = CustomPageNumberPagination

    def get_queryset(self) -> PageQuerySet:
        return BlogPostListPage.objects.live().only("id", "url_path", "title", "body")
