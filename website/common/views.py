from typing import Any

from django.http.response import HttpResponse
from django.views.defaults import ERROR_404_TEMPLATE_NAME
from django.views.generic import TemplateView

from website.home.models import HomePage


class Error404View(TemplateView):
    template_name = ERROR_404_TEMPLATE_NAME

    def render_to_response(self, context: dict, **response_kwargs: Any) -> HttpResponse:
        response_kwargs["status"] = 404
        return super().render_to_response(context, **response_kwargs)

    def get_context_data(self, **kwargs: dict) -> dict:
        context = super().get_context_data(**kwargs)
        context["homepage"] = HomePage.objects.live().get()
        return context


page_not_found = Error404View.as_view()
