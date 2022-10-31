from typing import Any

from django.db.models import Value
from django.http.request import HttpRequest
from rest_framework.filters import SearchFilter
from wagtail.query import PageQuerySet
from wagtail.search.utils import parse_query_string


class WagtailSearchFilter(SearchFilter):
    def filter_queryset(
        self, request: HttpRequest, queryset: PageQuerySet, view: Any
    ) -> PageQuerySet:
        search_query = request.query_params.get(self.search_param, "")

        if not search_query:
            return queryset.annotate(relevance=Value(0)).none()

        filters, query = parse_query_string(search_query)
        results = queryset.search(query, order_by_relevance=True)

        return results.get_queryset()
