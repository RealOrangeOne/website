from django.urls import path

from .views import pygments_styles

app_name = "code_block"

urlpatterns = [path("<slug:name>.css", pygments_styles, name="styles")]
