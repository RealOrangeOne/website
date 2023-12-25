from django.core.paginator import EmptyPage, Paginator
from django.http.request import HttpRequest
from django.http.response import Http404, HttpResponse, HttpResponseBadRequest
from django.template.response import TemplateResponse
from django.utils.decorators import method_decorator
from django.utils.functional import cached_property
from django.views.decorators.http import require_GET
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.models import Page
from wagtail.search.utils import parse_query_string

from website.common.models import BaseContentPage, BaseListingPage
from website.common.utils import get_page_models

from .serializers import MIN_SEARCH_LENGTH, SearchParamsSerializer


class SearchPage(RoutablePageMixin, BaseContentPage):
    max_count = 1
    subpage_types: list = []
    parent_page_types = ["home.HomePage"]
    PAGE_SIZE = 12

    # Exclude singleton pages from search results
    EXCLUDED_PAGE_TYPES = {
        *(page for page in get_page_models() if page.max_count == 1),
        BaseListingPage,
    }

    @cached_property
    def show_reading_time(self) -> bool:
        return False

    @cached_property
    def show_table_of_contents(self) -> bool:
        return False

    def get_context(self, request: HttpRequest) -> dict:
        context = super().get_context(request)
        context["search_query"] = request.GET.get("q", "")
        context["search_url"] = self.reverse_subpage("results")
        context["MIN_SEARCH_LENGTH"] = MIN_SEARCH_LENGTH
        context["SEO_INDEX"] = False
        return context

    @route(r"^results/$")
    @method_decorator(require_GET)
    def results(self, request: HttpRequest) -> HttpResponse:
        if not request.htmx:
            return HttpResponseBadRequest()

        serializer = SearchParamsSerializer(data=request.GET)

        if not serializer.is_valid():
            return TemplateResponse(
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
        pages = (
            Page.objects.live()
            .public()
            .not_type(self.__class__, *self.EXCLUDED_PAGE_TYPES)
            .search(query, order_by_relevance=True)
        )

        paginator = Paginator(pages, self.PAGE_SIZE)
        context["paginator"] = paginator

        try:
            results = paginator.page(page_num)

            # HACK: Search results aren't a queryset, so we can't call `.specific` on it. This forces it to one as efficiently as possible
            results.object_list = results.object_list.get_queryset().specific()

        except EmptyPage as e:
            raise Http404 from e

        context["results"] = results

        return TemplateResponse(request, "search/search_results.html", context)
