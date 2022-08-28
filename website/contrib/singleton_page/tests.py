from django.test import TestCase

from website.common.models import ContentPage
from website.home.models import HomePage

from .utils import SingletonPageCache


class SingletonURLTestCase(TestCase):
    def test_gets_url(self) -> None:
        with self.assertNumQueries(2):
            self.assertEqual(SingletonPageCache.get_url(HomePage), "http://localhost/")

    def test_missing_page(self) -> None:
        with self.assertNumQueries(1):
            self.assertIsNone(SingletonPageCache.get_url(ContentPage))
