from django.test import SimpleTestCase, TestCase
from django.urls import reverse


class Error404PageTestCase(TestCase):
    url = reverse("404")

    def test_accessible(self) -> None:
        response = self.client.get(self.url)
        self.assertContains(response, "<h1>There's nothing here!</h1>", html=True)

    def test_actual_404(self) -> None:
        response = self.client.get("/does-not-exist/")
        self.assertContains(
            response, "<h1>There's nothing here!</h1>", html=True, status_code=404
        )

    def test_queries(self) -> None:
        with self.assertNumQueries(8):
            self.client.get(self.url)


class RobotsViewTestCase(SimpleTestCase):
    url = reverse("robotstxt")

    def test_accessible(self) -> None:
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["sitemap"], "http://testserver/sitemap.xml")


class SecurityViewTestCase(TestCase):
    url = reverse("securitytxt")

    def test_accessible(self) -> None:
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context["security_txt"],
            "http://testserver/.well-known/security.txt",
        )
