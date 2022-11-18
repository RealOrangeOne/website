from unittest.mock import patch

from django.http.response import HttpResponse
from django.test import SimpleTestCase, TestCase, override_settings
from django.urls import reverse


class SecurityViewTestCase(TestCase):
    url = reverse("well-known:security-txt")

    def test_accessible(self) -> None:
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context["security_txt"],
            "http://testserver/.well-known/security.txt",
        )

    def test_cache(self) -> None:
        response = self.client.get(self.url)
        self.assertEqual(response["Cache-Control"], "max-age=302400")


class MatrixServerViewTestCase(SimpleTestCase):
    url = reverse("well-known:matrix-server")

    def test_accessible(self) -> None:
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")
        self.assertTemplateUsed(response, "well-known/matrix-server.json")


class MatrixClientViewTestCase(SimpleTestCase):
    url = reverse("well-known:matrix-client")

    def test_accessible(self) -> None:
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")
        self.assertTemplateUsed(response, "well-known/matrix-client.json")


class ActivityPubProxyView(TestCase):
    PROXIED_PATHS = [
        reverse("well-known:webfinger"),
        reverse("well-known:hostmeta"),
        reverse("well-known:nodeinfo"),
    ]

    def setUp(self) -> None:
        super().setUp()

        proxy_view_patcher = patch("website.well_known.views.proxy_view")
        self.proxy_view = proxy_view_patcher.start()
        self.addCleanup(proxy_view_patcher.stop)

        self.proxy_view.return_value = HttpResponse()

    @override_settings(ACTIVITYPUB_HOST="activitypub.example.com")
    def test_urls(self) -> None:
        for path in self.PROXIED_PATHS:
            with self.subTest(path):
                response = self.client.get(path)
                self.assertEqual(response.status_code, 200)
                self.assertEqual(
                    self.proxy_view.call_args[0][1],
                    f"https://activitypub.example.com{path}",
                )
                self.assertEqual(response["Cache-Control"], "max-age=60")

    @override_settings(ACTIVITYPUB_HOST="")
    def test_unconfigured(self) -> None:
        for path in self.PROXIED_PATHS:
            with self.subTest(path):
                response = self.client.get(path)
                self.assertEqual(response.status_code, 404)
                self.assertFalse(self.proxy_view.called)
