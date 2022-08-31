from django.test import TestCase
from django.urls import reverse

from .utils import PYGMENTS_VERSION_SLUG


class PygmentsStylesTestCase(TestCase):
    url = reverse("code-block:styles")

    def test_accessible(self) -> None:
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Cache-Control"], "max-age=3600")
        self.assertEqual(response["Content-Type"], "text/css")

    def test_url_contains_version(self) -> None:
        self.assertIn(PYGMENTS_VERSION_SLUG, self.url)
