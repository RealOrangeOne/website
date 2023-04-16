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

    def test_actual_404_no_url_match(self) -> None:
        response = self.client.get("/favicon.ico")
        self.assertContains(
            response, "<h1>There's nothing here!</h1>", html=True, status_code=404
        )

    def test_queries(self) -> None:
        with self.assertNumQueries(25):
            self.client.get(self.url)


class Error500PageTestCase(SimpleTestCase):
    url = reverse("500")

    def test_accessible(self) -> None:
        response = self.client.get(self.url)
        self.assertContains(
            response, "<h1>Internal server error</h1>", html=True, status_code=500
        )


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


class KeybaseViewTestCase(SimpleTestCase):
    url = reverse("keybase")

    def test_accessible(self) -> None:
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "I hereby claim")


class AllPagesFeedTestCase(TestCase):
    url = reverse("feed")

    def test_accessible(self) -> None:
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
