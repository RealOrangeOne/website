from django.core.paginator import EmptyPage, Paginator
from django.http.request import HttpRequest
from django.http.response import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.utils.functional import cached_property
from django.views.decorators.http import require_GET
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.models import Page
from wagtail.query import PageQuerySet
from wagtail.search.models import Query
from wagtail.search.utils import parse_query_string

from website.common.models import BaseContentMixin, BasePage
from website.common.utils import TocEntry
from website.home.models import HomePage

from .serializers import MIN_SEARCH_LENGTH, SearchParamsSerializer


class SearchPage(BaseContentMixin, RoutablePageMixin, BasePage):  # type: ignore[misc]
    max_count = 1
    subpage_types: list = []
    parent_page_types = ["home.HomePage"]
    content_panels = BasePage.content_panels + BaseContentMixin.content_panels
    search_fields = BasePage.search_fields + BaseContentMixin.search_fields
    PAGE_SIZE = 15

    @cached_property
    def reading_time(self) -> int:
        """
        How does one read a search page?
        """
        return 0

    @cached_property
    def table_of_contents(self) -> list[TocEntry]:
        return []

    def get_context(self, request: HttpRequest) -> dict:
        context = super().get_context(request)
        context["search_query"] = request.GET.get("q", "")
        context["search_url"] = self.reverse_subpage("results")
        context["MIN_SEARCH_LENGTH"] = MIN_SEARCH_LENGTH
        return context

    @route(r"^results/$")
    @method_decorator(require_GET)
    def results(self, request: HttpRequest) -> HttpResponse:
        if not request.htmx:
            return HttpResponseBadRequest()

        serializer = SearchParamsSerializer(data=request.GET)

        if not serializer.is_valid():
            return render(
                request,
                "search/enter-search-term.html",
                {"MIN_SEARCH_LENGTH": MIN_SEARCH_LENGTH},
            )

        search_query = serializer.validated_data["q"]
        page_num = serializer.validated_data["page"]

        context = {
            **self.get_context(request),
            "search_query": search_query,
            "page_num": page_num,
        }

        filters, query = parse_query_string(search_query)
        Query.get(search_query).add_hit()
        pages = Page.objects.live().not_type(self.__class__, HomePage).search(query)

        paginator = Paginator(pages, self.PAGE_SIZE)
        context["paginator"] = paginator

        try:
            results = paginator.page(page_num)

            # HACK: Search results aren't a queryset, so we can't call `.specific` on it. This forces it to one as efficiently as possible
            if not isinstance(results.object_list, PageQuerySet):
                results.object_list = Page.objects.filter(
                    id__in=list(
                        results.object_list.get_queryset().values_list("id", flat=True)
                    )
                ).specific()

        except EmptyPage:
            results = []

        context["results"] = results

        return render(request, "search/search_results.html", context)
