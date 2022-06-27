from django.test import TestCase
from django.urls import reverse
from pygments.styles import get_all_styles


class PygmentsStylesTestCase(TestCase):
    def test_accessible(self) -> None:
        for style in get_all_styles():
            with self.subTest(style=style):
                response = self.client.get(
                    reverse("static-pygments:styles", args=[style])
                )
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response["Cache-Control"], "max-age=3600, public")

    def test_unknown_style(self) -> None:
        response = self.client.get(
            reverse("static-pygments:styles", args=["not-a-style"])
        )
        self.assertEqual(response.status_code, 404)
