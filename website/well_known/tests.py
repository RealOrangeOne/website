from django.test import SimpleTestCase, TestCase
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
        self.assertTemplateUsed(response, "matrix-server.json")


class MatrixClientViewTestCase(SimpleTestCase):
    url = reverse("well-known:matrix-client")

    def test_accessible(self) -> None:
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")
        self.assertTemplateUsed(response, "matrix-client.json")
