from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http.request import HttpRequest
from django.utils.functional import cached_property
from wagtail.models import Page
from wagtail.query import PageQuerySet
from wagtail.search.models import Query
from wagtail.search.utils import parse_query_string

from website.common.models import BaseContentMixin, BasePage
from website.common.utils import TocEntry
from website.home.models import HomePage


class SearchPage(BaseContentMixin, BasePage):  # type: ignore[misc]
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

    def get_search_pages(self) -> PageQuerySet:
        return Page.objects.live().not_type(self.__class__, HomePage)

    def get_context(self, request: HttpRequest) -> dict:
        context = super().get_context(request)
        if query_string := request.GET.get("q", ""):
            filters, query = parse_query_string(query_string)
            Query.get(query_string).add_hit()
            pages = self.get_search_pages().search(query)
        else:
            pages = Page.objects.none()

        paginator = Paginator(pages, self.PAGE_SIZE)
        page_num = request.GET.get("page", "1")
        try:
            results = paginator.page(page_num)

            # HACK: Search results aren't a queryset, so we can't call `.specific` on it. This forces it to one as efficiently as possible
            if not isinstance(results.object_list, PageQuerySet):
                results.object_list = Page.objects.filter(
                    id__in=list(
                        results.object_list.get_queryset().values_list("id", flat=True)
                    )
                ).specific()
        except (PageNotAnInteger, EmptyPage):
            results = None
            context["invalid_page"] = True

        context["results"] = results

        return context
