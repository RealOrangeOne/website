from django.urls import path

from .utils import PYGMENTS_VERSION_SLUG
from .views import pygments_styles

app_name = "code-block"

urlpatterns = [
    # HACK: Bake the pygments version into the URL, without needing a custom method
    path(
        f"pygments-<slug:name>.{PYGMENTS_VERSION_SLUG}.css",
        pygments_styles,
        name="styles",
    )
]
