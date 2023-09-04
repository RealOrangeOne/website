from datetime import timedelta

from django.conf import settings
from django.http.request import HttpRequest
from django.http.response import Http404, HttpResponse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_control, cache_page
from django.views.generic import TemplateView
from proxy.views import proxy_view
from requests.exceptions import RequestException

from website.contact.models import ContactPage
from website.contrib.singleton_page.utils import SingletonPageCache


class SecurityView(TemplateView):
    template_name = "well-known/security.txt"
    content_type = "text/plain"

    expires = timedelta(days=7)

    @method_decorator(cache_control(max_age=int(expires.total_seconds() / 2)))
    def dispatch(self, request: HttpRequest) -> HttpResponse:
        return super().dispatch(request)

    def get_context_data(self, **kwargs: dict) -> dict:
        context = super().get_context_data(**kwargs)
        context["security_txt"] = self.request.build_absolute_uri(self.request.path)
        contact_page_path = SingletonPageCache.get_url(ContactPage, self.request)
        context["contact_page_url"] = (
            self.request.build_absolute_uri(contact_page_path)
            if contact_page_path
            else None
        )
        context["expires"] = (
            (timezone.now() + self.expires).replace(microsecond=0).isoformat()
        )
        return context


@method_decorator(cache_control(max_age=60 * 60), name="dispatch")
class MatrixServerView(TemplateView):
    template_name = "well-known/matrix-server.json"
    content_type = "application/json"


@method_decorator(cache_control(max_age=60 * 60), name="dispatch")
class MatrixClientView(TemplateView):
    template_name = "well-known/matrix-client.json"
    content_type = "application/json"


@cache_page(60)
def activitypub_proxy(request: HttpRequest) -> HttpResponse:
    if not settings.ACTIVITYPUB_HOST:
        raise Http404

    try:
        return proxy_view(
            request,
            f"https://{settings.ACTIVITYPUB_HOST}{request.path}",
        )
    except RequestException:
        return HttpResponse(status_code=502)
