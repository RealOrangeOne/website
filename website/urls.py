import re

from django.conf import settings
from django.urls import include, path, re_path
from django.views.decorators.cache import cache_control, cache_page
from django.views.defaults import server_error
from django.views.static import serve
from wagtail import urls as wagtail_urls
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.contrib.sitemaps.views import sitemap
from wagtail.documents import urls as wagtaildocs_urls
from wagtail.images.views.serve import ServeView
from wagtail_favicon.urls import urls as favicon_urls
from wagtailautocomplete.urls.admin import urlpatterns as autocomplete_admin_urls

from website.common.views import AllPagesFeed, KeybaseView, RobotsView, page_not_found

urlpatterns = [
    path("admin/autocomplete/", include(autocomplete_admin_urls)),
    path("admin/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    path(
        "code-block/",
        include("website.contrib.code_block.urls"),
    ),
    path(".well-known/", include("website.well_known.urls")),
    re_path(
        r"^images/([^/]*)/(\d*)/([^/]*)/[^/]*$",
        ServeView.as_view(action="redirect"),
        name="wagtailimages_serve",
    ),
    path("sitemap.xml", cache_page(60 * 60)(sitemap), name="sitemap"),
    path(
        "robots.txt",
        RobotsView.as_view(),
        name="robotstxt",
    ),
    path(
        "keybase.txt",
        KeybaseView.as_view(),
        name="keybase",
    ),
    path("404/", page_not_found, name="404"),
    path("500/", server_error, name="500"),
    path("feed/", AllPagesFeed(), name="feed"),
    path(".health/", include("health_check.urls")),
    path("", include("website.legacy.urls")),
    path("api/", include("website.api.urls")),
    path("", include(favicon_urls)),
    # Some say it's a bad idea to serve media with Django - I don't care
    re_path(
        r"^%s(?P<path>.*)$" % re.escape(settings.MEDIA_URL.lstrip("/")),
        cache_control(max_age=60 * 60)(serve),
        {"document_root": settings.MEDIA_ROOT},
    ),
]


if not settings.DEBUG:
    handler404 = "website.common.views.page_not_found"


if settings.DEBUG:
    # Add django-browser-reload
    urlpatterns.append(path("__reload__/", include("django_browser_reload.urls")))

    # Add django-debug-toolbar
    urlpatterns.append(path("__debug__/", include("debug_toolbar.urls")))

urlpatterns = urlpatterns + [
    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's page serving mechanism. This should be the last pattern in
    # the list:
    path("", include(wagtail_urls)),
    # Alternatively, if you want Wagtail pages to be served from a subpath
    # of your site, rather than the site root:
    #    path("pages/", include(wagtail_urls)),
]
