from pathlib import Path

import environ
from whitenoise.compress import Compressor as WhitenoiseCompressor

BASE_DIR = Path(__file__).parent.parent

env = environ.Env(
    DEBUG=(bool, False),
    BASE_HOSTNAME=(str, "example.com"),
    UNSPLASH_CLIENT_ID=(str, ""),
    SPOTIFY_PROXY_HOST=(str, ""),
    SEO_INDEX=(bool, False),
    SENTRY_DSN=(str, ""),
    TEST=(bool, False),
)

# Read local secrets
environ.Env.read_env(BASE_DIR / ".env")

DEBUG = env("DEBUG")
TEST = env("TEST")

SECRET_KEY = env("SECRET_KEY")

BASE_HOSTNAME = env("BASE_HOSTNAME")
ALLOWED_HOSTS = ["*"] if DEBUG else [BASE_HOSTNAME]

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
    "website.utils",
    "website.well_known",
    "website.legacy",
    "website.contrib.code_block",
    "website.contrib.mermaid_block",
    "website.contrib.unsplash",
    "website.contrib.singleton_page",
    "website.contrib.wagtail_cache_purge",
    "wagtail.contrib.forms",
    "wagtail.contrib.redirects",
    "wagtail.contrib.modeladmin",
    "wagtail.contrib.routable_page",
    "wagtail.contrib.typed_table_block",
    "wagtail.contrib.settings",
    "wagtail.embeds",
    "wagtail.sites",
    "wagtail.users",
    "wagtail.snippets",
    "wagtail.documents",
    "wagtail.images",
    "wagtail.search",
    "wagtail.admin",
    "wagtail",
    "wagtailmetadata",
    "modelcluster",
    "taggit",
    "generic_chooser",
    "wagtail_draftail_snippet",
    "wagtailautocomplete",
    "django_rq",
    "rest_framework",
    "corsheaders",
    "wagtail_favicon",
    "plausible",
    "plausible.contrib.wagtail",
    "sri",
    "wagtail_2fa",
    "django_otp",
    "django_otp.plugins.otp_totp",
    "health_check",
    "health_check.db",
    "health_check.cache",
    "health_check.storage",
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
    "corsheaders.middleware.CorsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "wagtail_2fa.middleware.VerifyUserMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "wagtail.contrib.redirects.middleware.RedirectMiddleware",
    "django_htmx.middleware.HtmxMiddleware",
    "csp.middleware.CSPMiddleware",
    "django_permissions_policy.PermissionsPolicyMiddleware",
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
                "website.utils.context_processors.global_vars",
            ],
        },
    },
]

WSGI_APPLICATION = "website.wsgi.application"


DATABASES = {"default": env.db(default=f"sqlite:///{BASE_DIR}/db.sqlite3")}

CACHES = {
    "default": env.cache(default="dummycache://"),
    "renditions": env.cache(
        var="RENDITION_CACHE_URL", default="locmemcache://renditions"
    ),
}

# Allow the redirect importer to work in load-balanced / cloud environments.
# https://docs.wagtail.io/en/v2.13/reference/settings.html#redirects
WAGTAIL_REDIRECTS_FILE_STORAGE = "cache"

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

WAGTAIL_2FA_REQUIRED = not DEBUG

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

WHITENOISE_ALLOW_ALL_ORIGINS = False

WHITENOISE_SKIP_COMPRESS_EXTENSIONS = list(
    WhitenoiseCompressor.SKIP_COMPRESS_EXTENSIONS
) + ["map"]

MEDIA_ROOT = BASE_DIR / "media"
MEDIA_URL = "/media/"

WAGTAILIMAGES_FORMAT_CONVERSIONS = {
    "webp": "webp",
    "jpeg": "webp",
    "png": "webp",
}

# Wagtail settings

WAGTAIL_SITE_NAME = "website"

# Search
# https://docs.wagtail.org/en/stable/topics/search/backends.html
WAGTAILSEARCH_BACKENDS = {
    "default": {
        "BACKEND": "wagtail.search.backends.database",
        "AUTO_UPDATE": True,
        "ATOMIC_REBUILD": True,
    }
}

WAGTAILADMIN_BASE_URL = f"https://{BASE_HOSTNAME}"

CORS_ALLOWED_ORIGINS = [WAGTAILADMIN_BASE_URL, "https://editor.swagger.io"]

WAGTAIL_ENABLE_UPDATE_CHECK = False

WAGTAIL_FRONTEND_LOGIN_URL = "/admin/login/"
PASSWORD_REQUIRED_TEMPLATE = "password_required.html"

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

WAGTAILADMIN_RICH_TEXT_EDITORS = {
    "default": {
        "WIDGET": "wagtail.admin.rich_text.DraftailRichTextArea",
        "OPTIONS": {
            "features": [
                "h2",
                "h3",
                "h4",
                "h5",
                "h6",
                "bold",
                "italic",
                "ol",
                "ul",
                "link",
                "document-link",
                "code",
                "strikethrough",
                "snippet-link",
                "snippet-embed",
                "superscript",
                "subscript",
                "blockquote",
            ]
        },
    },
    "plain": {
        "WIDGET": "wagtail.admin.rich_text.DraftailRichTextArea",
        "OPTIONS": {
            "features": [
                "bold",
                "italic",
                "link",
                "document-link",
                "code",
                "strikethrough",
                "snippet-link",
                "superscript",
                "subscript",
            ]
        },
    },
    "simple": {
        "WIDGET": "wagtail.admin.rich_text.DraftailRichTextArea",
        "OPTIONS": {
            "features": [
                "bold",
                "italic",
                "ol",
                "ul",
                "link",
                "document-link",
                "code",
                "strikethrough",
                "snippet-link",
                "superscript",
                "subscript",
            ]
        },
    },
}

WAGTAIL_PASSWORD_RESET_ENABLED = False
WAGTAIL_WORKFLOW_ENABLED = False
WAGTAIL_MODERATION_ENABLED = False

UNSPLASH_CLIENT_ID = env("UNSPLASH_CLIENT_ID")
SPOTIFY_PROXY_HOST = env("SPOTIFY_PROXY_HOST")

SEO_INDEX = env("SEO_INDEX")

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

    CORS_ALLOWED_ORIGINS = []
    CORS_ALLOW_ALL_ORIGINS = True

SWAGGER_SETTINGS = {"USE_SESSION_AUTH": False, "SECURITY_DEFINITIONS": {}}

REST_FRAMEWORK = {
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.AnonRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {
        "anon": "10/min",
    },
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
    ],
}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        # Send logs with at least INFO level to the console.
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "formatters": {
        "verbose": {
            "format": "[%(asctime)s][%(process)d][%(levelname)s][%(name)s] %(message)s"
        }
    },
    "loggers": {
        "website": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "wagtail": {
            "handlers": ["console"],
            "level": "WARNING",
            "propagate": False,
        },
        "django.request": {
            "handlers": ["console"],
            "level": "ERROR",
            "propagate": False,
        },
        "django.security": {
            "handlers": ["console"],
            "level": "WARNING",
            "propagate": False,
        },
    },
}


SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"
SECURE_REFERRER_POLICY = "same-origin"

SESSION_COOKIE_SECURE = not DEBUG
SESSION_COOKIE_AGE = 2419200  # About a month
CSRF_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_HTTPONLY = True

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

PERMISSIONS_POLICY = {
    "accelerometer": [],
    "ambient-light-sensor": [],
    "autoplay": [],
    "camera": [],
    "display-capture": [],
    "document-domain": [],
    "encrypted-media": [],
    "fullscreen": [],
    "geolocation": [],
    "gyroscope": [],
    "interest-cohort": [],
    "magnetometer": [],
    "microphone": [],
    "midi": [],
    "payment": [],
    "usb": [],
}

if not DEBUG:
    SECURE_HSTS_SECONDS = 2592000  # 30 days

    CSP_BLOCK_ALL_MIXED_CONTENT = True
    CSP_UPGRADE_INSECURE_REQUESTS = True

if sentry_dsn := env("SENTRY_DSN"):
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration
    from sentry_sdk.integrations.redis import RedisIntegration
    from sentry_sdk.integrations.rq import RqIntegration
    from sentry_sdk.utils import get_default_release

    sentry_kwargs = {
        "dsn": sentry_dsn,
        "integrations": [DjangoIntegration(), RqIntegration(), RedisIntegration()],
        "release": get_default_release(),
    }

    sentry_sdk.init(**sentry_kwargs)
