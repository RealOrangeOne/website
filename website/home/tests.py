from django.test import TestCase

from .models import HomePage


class HomePageTestCase(TestCase):
    page: HomePage

    @classmethod
    def setUpTestData(cls) -> None:
        cls.page = HomePage.objects.get()

    def test_accessible(self) -> None:
        response = self.client.get(self.page.url)
        self.assertEqual(response.status_code, 200)
