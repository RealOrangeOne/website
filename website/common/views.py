from datetime import timedelta
from typing import Any

from django.http.response import HttpResponse
from django.urls import reverse
from django.utils import timezone
from django.views.defaults import ERROR_404_TEMPLATE_NAME
from django.views.generic import TemplateView

from website.contact.models import ContactPage
from website.home.models import HomePage


class Error404View(TemplateView):
    template_name = ERROR_404_TEMPLATE_NAME

    def render_to_response(self, context: dict, **response_kwargs: Any) -> HttpResponse:
        if self.request.resolver_match.url_name != "404":
            response_kwargs["status"] = 404
        return super().render_to_response(context, **response_kwargs)

    def get_context_data(self, **kwargs: dict) -> dict:
        context = super().get_context_data(**kwargs)
        context["homepage"] = HomePage.objects.live().get()
        return context


page_not_found = Error404View.as_view()


class RobotsView(TemplateView):
    template_name = "robots.txt"
    content_type = "text/plain"

    def get_context_data(self, **kwargs: dict) -> dict:
        context = super().get_context_data(**kwargs)
        context["sitemap"] = self.request.build_absolute_uri(reverse("sitemap"))
        return context


class SecurityView(TemplateView):
    template_name = "security.txt"
    content_type = "text/plain"

    expires = timedelta(days=7)

    def get_context_data(self, **kwargs: dict) -> dict:
        context = super().get_context_data(**kwargs)
        context["security_txt"] = self.request.build_absolute_uri(
            reverse("securitytxt")
        )
        context["contact_page"] = ContactPage.objects.live().first()
        context["expires"] = (
            (timezone.now() + self.expires).replace(microsecond=0).isoformat()
        )
        return context
