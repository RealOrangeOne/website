from django.test import SimpleTestCase, TestCase, override_settings
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

    @override_settings(SEO_INDEX=True)
    def test_accessible(self) -> None:
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["sitemap"], "http://testserver/sitemap.xml")
        self.assertContains(response, "Allow: /")
        self.assertTrue(response.context["SEO_INDEX"])

    @override_settings(SEO_INDEX=False)
    def test_disallow(self) -> None:
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Disallow: /")
        self.assertFalse(response.context["SEO_INDEX"])


class SecurityViewTestCase(TestCase):
    url = reverse("securitytxt")

    def test_accessible(self) -> None:
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context["security_txt"],
            "http://testserver/.well-known/security.txt",
        )


class MatrixServerViewTestCase(SimpleTestCase):
    url = reverse("matrix-server")

    def test_accessible(self) -> None:
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")
        self.assertTemplateUsed(response, "matrix-server.json")


class MatrixClientViewTestCase(SimpleTestCase):
    url = reverse("matrix-client")

    def test_accessible(self) -> None:
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")
        self.assertTemplateUsed(response, "matrix-client.json")
