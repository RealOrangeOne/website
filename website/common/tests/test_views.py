from django.test import SimpleTestCase, TestCase
from django.urls import reverse


class Error404PageTestCase(TestCase):
    url = reverse("404")

    def test_accessible(self) -> None:
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 404)

    def test_queries(self) -> None:
        with self.assertNumQueries(10):
            self.client.get(self.url)


class RobotsViewTestCase(SimpleTestCase):
    url = reverse("robotstxt")

    def test_accessible(self) -> None:
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
