from django.test import TestCase
from django.urls import reverse

from website.blog.factories import BlogPostListPageFactory
from website.home.models import HomePage


class PostsFeedViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.home_page = HomePage.objects.get()
        cls.page = BlogPostListPageFactory(parent=cls.home_page)

    def test_redirects(self) -> None:
        response = self.client.get("/posts/index.xml")
        self.assertRedirects(
            response, self.page.url + self.page.reverse_subpage("feed"), status_code=301
        )


class AllPagesFeedViewTestCase(TestCase):
    def test_redirects(self) -> None:
        response = self.client.get("/index.xml")
        self.assertRedirects(response, reverse("feed"), status_code=301)
