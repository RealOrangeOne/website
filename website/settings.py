from pathlib import Path

import environ
from whitenoise.compress import Compressor as WhitenoiseCompressor

BASE_DIR = Path(__file__).parent.parent

env = environ.Env(
    DEBUG=(bool, False),
    BASE_HOSTNAME=(str, "example.com"),
    UNSPLASH_CLIENT_ID=(str, ""),
    SPOTIFY_PROXY_HOST=(str, ""),
)

# Read local secrets
environ.Env.read_env(BASE_DIR / ".env")

DEBUG = env("DEBUG")

SECRET_KEY = env("SECRET_KEY")

ALLOWED_HOSTS = ["*"]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Application definition
INSTALLED_APPS = [
    "website.common",
    "website.home",
    "website.search",
    "website.blog",
    "website.images",
    "website.contact",
    "website.spotify",
    "website.contrib.code_block",
    "website.contrib.mermaid_block",
    "website.contrib.unsplash",
    "wagtail.contrib.forms",
    "wagtail.contrib.redirects",
    "wagtail.contrib.modeladmin",
    "wagtail.contrib.routable_page",
    "wagtail.embeds",
    "wagtail.sites",
    "wagtail.users",
    "wagtail.snippets",
    "wagtail.documents",
    "wagtail.images",
    "wagtail.search",
    "wagtail.admin",
    "wagtail",
    "modelcluster",
    "taggit",
    "generic_chooser",
    "wagtail_draftail_snippet",
    "django_rq",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.sitemaps",
    "whitenoise.runserver_nostatic",
    "django.contrib.staticfiles",
]

MIDDLEWARE = [
    "django.middleware.gzip.GZipMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "wagtail.contrib.redirects.middleware.RedirectMiddleware",
    "django_htmx.middleware.HtmxMiddleware",
]

ROOT_URLCONF = "website.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "website.wsgi.application"


DATABASES = {"default": env.db(default=f"sqlite:///{BASE_DIR}/db.sqlite3")}

CACHES = {"default": env.cache(default="dummycache://")}

RQ_QUEUES = {}

USE_REDIS_QUEUE = False
if queue_store := env.cache("QUEUE_STORE_URL", default=None):
    CACHES["rq"] = queue_store
    USE_REDIS_QUEUE = True
    RQ_QUEUES["default"] = {"USE_REDIS_CACHE": "rq"}


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = "en-gb"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

STATICFILES_DIRS = [
    BASE_DIR / "static" / "build",
]

if not DEBUG:
    STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

STATIC_ROOT = BASE_DIR / "collected-static"
STATIC_URL = "/static/"

WHITENOISE_SKIP_COMPRESS_EXTENSIONS = list(
    WhitenoiseCompressor.SKIP_COMPRESS_EXTENSIONS
) + ["map"]

MEDIA_ROOT = BASE_DIR / "media"
MEDIA_URL = "/media/"


# Wagtail settings

WAGTAIL_SITE_NAME = "website"

# Search
# https://docs.wagtail.org/en/stable/topics/search/backends.html
WAGTAILSEARCH_BACKENDS = {
    "default": {
        "BACKEND": "wagtail.search.backends.database",
        "AUTO_UPDATE": DEBUG,
        "ATOMIC_REBUILD": True,
    }
}

BASE_HOSTNAME = env("BASE_HOSTNAME")
WAGTAILADMIN_BASE_URL = f"https://{BASE_HOSTNAME}"

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

WAGTAILIMAGES_IMAGE_MODEL = "images.CustomImage"

WAGTAILEMBEDS_FINDERS = [
    {
        "class": "website.common.embed.YouTubeLiteEmbedFinder",
    },
    {
        "class": "wagtail.embeds.finders.oembed",
    },
]

UNSPLASH_CLIENT_ID = env("UNSPLASH_CLIENT_ID")
SPOTIFY_PROXY_HOST = env("SPOTIFY_PROXY_HOST")


if DEBUG:
    # Add django-browser-reload
    INSTALLED_APPS.append("django_browser_reload")
    MIDDLEWARE.append("django_browser_reload.middleware.BrowserReloadMiddleware")

    # Add django-debug-toolbar
    INSTALLED_APPS.append("debug_toolbar")
    MIDDLEWARE.append("debug_toolbar.middleware.DebugToolbarMiddleware")
    DEBUG_TOOLBAR_CONFIG = {
        "SHOW_TOOLBAR_CALLBACK": "website.common.utils.show_toolbar_callback",
        "RESULTS_CACHE_SIZE": 5,
        "SHOW_COLLAPSED": True,
    }

    # Add Wagtail styleguide
    INSTALLED_APPS.append("wagtail.contrib.styleguide")
