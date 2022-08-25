from typing import Type

from django.core.exceptions import ValidationError
from django.http.response import Http404
from django.utils.html import format_html
from wagtail.admin.forms.models import WagtailAdminModelForm
from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register
from wagtail.contrib.modeladmin.views import CreateView, EditView, IndexView
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


class UnsplashPhotoIndexView(IndexView):
    def get_buttons_for_obj(self, obj: UnsplashPhoto) -> list:
        buttons = super().get_buttons_for_obj(obj)
        assert buttons[0]["label"] == "Edit"
        buttons.pop(0)
        return buttons


class UnsplashPhotoEditView(EditView):
    """
    Prevent access to the edit view
    """

    def dispatch(self, *args: list, **kwargs: dict) -> None:
        raise Http404


@modeladmin_register
class UnsplashPhotoAdmin(ModelAdmin):
    model = UnsplashPhoto
    list_display = ["unsplash_id", "thumbnail", "description", "data_last_updated"]
    form_fields_exclude = ["data"]
    search_fields = ["unsplash_id", "data__description"]
    create_view_class = UnsplashPhotoCreateView
    index_view_class = UnsplashPhotoIndexView
    edit_view_class = UnsplashPhotoEditView
    menu_icon = "image"

    def description(self, instance: UnsplashPhoto) -> str:
        return instance.get_description()

    def thumbnail(self, instance: UnsplashPhoto) -> str:
        return format_html(
            "<img src='{}' width=165 class='admin-thumb' loading='lazy' decoding='async' />",
            instance.get_thumbnail_url(),
        )


@hooks.register("register_admin_viewset")
def register_person_chooser_viewset() -> UnsplashPhotoChooserViewSet:
    return UnsplashPhotoChooserViewSet(
        "unsplash_photo_chooser", url_prefix="unsplash-photo-chooser"
    )
