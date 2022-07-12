from typing import Type

from django.core.exceptions import ValidationError
from wagtail.admin.forms.models import WagtailAdminModelForm
from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register
from wagtail.contrib.modeladmin.views import CreateView
from wagtail.core import hooks

from .models import UnsplashPhoto
from .utils import get_unsplash_photo
from .views import UnsplashPhotoChooserViewSet


class UnsplashPhotoCreateView(CreateView):
    def get_form_class(self) -> WagtailAdminModelForm:
        """
        Modify form class to validate unsplash id and save data to model1
        """
        EditHandlerForm: Type[
            WagtailAdminModelForm
        ] = self.edit_handler.get_form_class()

        class CreateFormClass(EditHandlerForm):  # type: ignore[valid-type,misc]
            def clean(self) -> None:
                cleaned_data = super().clean()
                try:
                    self._unsplash_photo_data = get_unsplash_photo(
                        cleaned_data["unsplash_id"]
                    )
                except ValueError as e:
                    raise ValidationError(str(e))

            def save(self, commit: bool = True) -> UnsplashPhoto:
                self.instance.data = self._unsplash_photo_data
                return super().save(commit)

        return CreateFormClass


@modeladmin_register
class UnsplashPhotoAdmin(ModelAdmin):
    model = UnsplashPhoto
    list_display = ["unsplash_id", "description"]
    form_fields_exclude = ["data"]
    search_fields = ["unsplash_id", "data__description"]
    create_view_class = UnsplashPhotoCreateView
    menu_icon = "image"

    def description(self, instance: UnsplashPhoto) -> str:
        return instance.get_description()


@hooks.register("register_admin_viewset")
def register_person_chooser_viewset() -> UnsplashPhotoChooserViewSet:
    return UnsplashPhotoChooserViewSet(
        "unsplash_photo_chooser", url_prefix="unsplash-photo-chooser"
    )
