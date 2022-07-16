from django.test import TestCase
from django.urls import reverse
from pygments.styles import get_all_styles

from .utils import PYGMENTS_VERSION, PYGMENTS_VERSION_SLUG


class PygmentsStylesTestCase(TestCase):
    def test_accessible(self) -> None:
        for style in get_all_styles():
            with self.subTest(style=style):
                response = self.client.get(reverse("code-block:styles", args=[style]))
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response["Cache-Control"], "max-age=3600, public")
                self.assertEqual(response["ETag"], f'"{PYGMENTS_VERSION}"')

    def test_unknown_style(self) -> None:
        response = self.client.get(reverse("code-block:styles", args=["not-a-style"]))
        self.assertEqual(response.status_code, 404)

    def test_url_contains_version(self) -> None:
        for style in get_all_styles():
            with self.subTest(style=style):
                url = reverse("code-block:styles", args=[style])
                self.assertIn(PYGMENTS_VERSION_SLUG, url)
