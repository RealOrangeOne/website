from datetime import timedelta

from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import TemplateView

from website.contact.models import ContactPage


class SecurityView(TemplateView):
    template_name = "security.txt"
    content_type = "text/plain"

    expires = timedelta(days=7)

    @method_decorator(cache_page(int(expires.total_seconds() / 2)))
    def dispatch(self, request: HttpRequest) -> HttpResponse:
        return super().dispatch(request)

    def get_context_data(self, **kwargs: dict) -> dict:
        context = super().get_context_data(**kwargs)
        context["security_txt"] = self.request.build_absolute_uri(self.request.path)
        context["contact_page"] = ContactPage.objects.live().first()
        context["expires"] = (
            (timezone.now() + self.expires).replace(microsecond=0).isoformat()
        )
        return context


@method_decorator(cache_page(60 * 60), name="dispatch")
class MatrixServerView(TemplateView):
    template_name = "matrix-server.json"
    content_type = "application/json"


@method_decorator(cache_page(60 * 60), name="dispatch")
class MatrixClientView(TemplateView):
    template_name = "matrix-client.json"
    content_type = "application/json"
