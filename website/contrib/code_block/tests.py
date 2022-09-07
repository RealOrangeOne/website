from django.test import SimpleTestCase
from django.urls import reverse

from .blocks import CodeStructValue, get_language_choices
from .utils import PYGMENTS_VERSION_SLUG


class PygmentsStylesTestCase(SimpleTestCase):
    url = reverse("code-block:styles")

    def test_accessible(self) -> None:
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Cache-Control"], "max-age=3600")
        self.assertEqual(response["Content-Type"], "text/css")

    def test_url_contains_version(self) -> None:
        self.assertIn(PYGMENTS_VERSION_SLUG, self.url)


class CodeStructValueTestCase(SimpleTestCase):
    def test_highlights(self) -> None:
        for language, _ in get_language_choices():
            with self.subTest(language):
                block = CodeStructValue(
                    None, [("source", "test"), ("language", language)]
                )
                self.assertIsInstance(block.code(), str)
