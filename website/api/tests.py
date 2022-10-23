from django.urls import reverse
from rest_framework.test import APISimpleTestCase, APITestCase

from website.blog.factories import BlogPostPageFactory
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
        with self.assertNumQueries(4):
            response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)


class LMOTFYAPIViewTestCase(APITestCase):
    url = reverse("api:lmotfy")

    @classmethod
    def setUpTestData(cls) -> None:
        cls.home_page = HomePage.objects.get()

        for i in range(4):
            BlogPostPageFactory(parent=cls.home_page, title=f"Post {i}")

        cls.exact = BlogPostPageFactory(parent=cls.home_page, title="Post exact")

    def test_accessible(self) -> None:
        with self.assertNumQueries(5):
            response = self.client.get(self.url, {"search": "Post"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 5)

    def test_case_insensitive_search(self) -> None:
        with self.assertNumQueries(5):
            response = self.client.get(self.url, {"search": "post"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 5)

    def test_no_search_term(self) -> None:
        with self.assertNumQueries(1):
            response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_empty_search_term(self) -> None:
        with self.assertNumQueries(1):
            response = self.client.get(self.url, {"search": ""})
        self.assertEqual(response.status_code, 200)

    def test_exact(self) -> None:
        with self.assertNumQueries(5):
            response = self.client.get(self.url, {"search": "Post exact"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 1)

        result = response.data["results"][0]

        self.assertEqual(result["title"], "Post exact")
        self.assertEqual(result["full_url"], self.exact.full_url)
        self.assertEqual(result["date"], self.exact.date.isoformat())


class SchemaTestCase(APISimpleTestCase):
    def test_schema_redirect(self) -> None:
        response = self.client.get(reverse("api:index"), follow=False)
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("api:schema"), response.url)

    def test_schema(self) -> None:
        response = self.client.get(reverse("api:schema"))
        self.assertEqual(response.status_code, 200)
