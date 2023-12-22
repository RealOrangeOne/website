from django.test import TestCase
from django.urls import reverse


class AllPagesFeedViewTestCase(TestCase):
    def test_redirects(self) -> None:
        response = self.client.get("/index.xml")
        self.assertRedirects(
            response, reverse("feed"), status_code=301, fetch_redirect_response=True
        )

    def test_redirects_posts(self) -> None:
        response = self.client.get("/posts/index.xml")
        self.assertRedirects(
            response, reverse("feed"), status_code=301, fetch_redirect_response=True
        )
