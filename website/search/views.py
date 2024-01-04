from django.http import HttpRequest, JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_control
from django.views.generic import TemplateView, View
from wagtail.search.utils import parse_query_string
from wagtail_favicon.models import FaviconSettings
from wagtail_favicon.utils import get_rendition_url

from website.common.utils import get_site_title
from website.contrib.singleton_page.utils import SingletonPageCache

from .models import SearchPage
from .serializers import SearchParamsSerializer


@method_decorator(cache_control(max_age=60 * 60), name="dispatch")
class OpenSearchView(TemplateView):
    template_name = "search/opensearch.xml"
    content_type = "application/xml"

    def get_context_data(self, **kwargs: dict) -> dict:
        context = super().get_context_data(**kwargs)

        favicon_settings = FaviconSettings.for_request(self.request)

        if favicon_settings.base_favicon_image_id:
            context["favicon_url"] = self.request.build_absolute_uri(
                get_rendition_url(
                    favicon_settings.base_favicon_image, "fill-100|format-png"
                )
            )

        context["search_page_url"] = self.request.build_absolute_uri(
            SingletonPageCache.get_url(SearchPage, self.request)
        )
        context["search_suggestions_url"] = self.request.build_absolute_uri(
            reverse("opensearch-suggestions")
        )

        context["site_title"] = get_site_title()

        return context


@method_decorator(cache_control(max_age=60 * 60), name="dispatch")
class OpenSearchSuggestionsView(View):
    def get(self, request: HttpRequest) -> JsonResponse:
        serializer = SearchParamsSerializer(data=request.GET)

        if not serializer.is_valid():
            return JsonResponse(serializer.errors, status=400)

        search_page = get_object_or_404(SearchPage)

        filters, query = parse_query_string(serializer.validated_data["q"])

        results = (
            search_page.get_listing_pages()
            .search(query, order_by_relevance=True)[:5]
            .get_queryset()
        )

        return JsonResponse(
            [
                serializer.validated_data["q"],
                list(results.values_list("title", flat=True)),
            ],
            safe=False,
        )
