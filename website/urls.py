from django.conf import settings
from django.urls import include, path, re_path
from django.views.decorators.cache import cache_page
from wagtail import urls as wagtail_urls
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.contrib.sitemaps.views import sitemap
from wagtail.documents import urls as wagtaildocs_urls
from wagtail.images.views.serve import ServeView

from website.common.views import (
    MatrixServerView,
    RobotsView,
    SecurityView,
    page_not_found,
)

urlpatterns = [
    path("admin/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    path(
        "code-block/",
        include("website.contrib.code_block.urls"),
    ),
    re_path(
        r"^images/([^/]*)/(\d*)/([^/]*)/[^/]*$",
        ServeView.as_view(action="redirect"),
        name="wagtailimages_serve",
    ),
    path("sitemap.xml", cache_page(60 * 60)(sitemap), name="sitemap"),
    path("robots.txt", cache_page(60 * 60)(RobotsView.as_view()), name="robotstxt"),
    path(
        ".well-known/security.txt",
        cache_page(SecurityView.expires.total_seconds() / 2)(SecurityView.as_view()),
        name="securitytxt",
    ),
    path(
        ".well-known/matrix/server",
        cache_page(60 * 60)(MatrixServerView.as_view()),
        name="matrix-server",
    ),
    path("404/", page_not_found, name="404"),
]


if not settings.DEBUG:
    handler404 = "website.common.views.page_not_found"


if settings.DEBUG:
    from django.conf.urls.static import static

    # Serve media files from development server
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

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
