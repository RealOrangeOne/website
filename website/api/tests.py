from django.urls import reverse
from rest_framework.test import APISimpleTestCase, APITestCase

from website.common.factories import ContentPageFactory
from website.home.models import HomePage


class PingAPIViewTestCase(APISimpleTestCase):
    url = reverse("api:ping")

    def test_accessible(self) -> None:
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)


class PageLinksAPIViewTestCase(APITestCase):
    url = reverse("api:page-links")

    @classmethod
    def setUpTestData(cls) -> None:
        cls.home_page = HomePage.objects.get()

        for _ in range(5):
            ContentPageFactory(parent=cls.home_page)

    def test_accessible(self) -> None:
        with self.assertNumQueries(3):
            response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
