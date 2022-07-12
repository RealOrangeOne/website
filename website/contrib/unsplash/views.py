from generic_chooser.views import (
    ModelChooserCreateTabMixin,
    ModelChooserMixin,
    ModelChooserViewSet,
)

from .models import UnsplashPhoto


class UnsplashPhotoCreateTabMixin(ModelChooserCreateTabMixin):
    """
    Don't allow creation during creation
    """

    def get_form_class(self) -> None:
        return None


class UnsplashPhotoChooserMixin(ModelChooserMixin):
    results_template = "unsplash/results.html"

    def get_object_string(self, instance: UnsplashPhoto) -> str:
        """
        Just use the description. It doesn't like showing HTML here
        """
        return instance.get_description()

    def get_row_data(self, item: UnsplashPhoto) -> dict:
        item_data = super().get_row_data(item)
        item_data["item"] = item
        return item_data


class UnsplashPhotoChooserViewSet(ModelChooserViewSet):
    icon = "image"
    model = UnsplashPhoto
    page_title = "Choose a photo"
    per_page = 10
    order_by = "unsplash_id"
    fields = ["unsplash_id", "data"]
    create_tab_mixin_class = UnsplashPhotoCreateTabMixin
    chooser_mixin_class = UnsplashPhotoChooserMixin
