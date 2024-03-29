from django.utils.html import format_html
from generic_chooser.widgets import AdminChooser

from .models import UnsplashPhoto


class UnsplashPhotoChooser(AdminChooser):
    choose_one_text = "Choose a photo"
    choose_another_text = "Choose another photo"
    show_edit_link = False
    show_create_link = False
    model = UnsplashPhoto
    choose_modal_url_name = "unsplash_photo_chooser:choose"

    def get_title(self, instance: UnsplashPhoto) -> str:
        return format_html(
            "<img src='{}' width=165 loading='lazy' decoding='async' referrerpolicy='no-referrer'>",
            instance.get_thumbnail_url(),
        )
