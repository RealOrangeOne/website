from django.test import TestCase

from website.home.models import HomePage

from .factories import BlogPostListPageFactory, BlogPostPageFactory


class BlogPostPageTestCase(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.home_page = HomePage.objects.get()
        cls.blog_post_list_page = BlogPostListPageFactory(parent=cls.home_page)
        cls.page = BlogPostPageFactory(parent=cls.blog_post_list_page)

    def test_accessible(self) -> None:
        response = self.client.get(self.page.url)
        self.assertEqual(response.status_code, 200)

    def test_queries(self) -> None:
        with self.assertNumQueries(45):
            self.client.get(self.page.url)


class BlogPostListPageTestCase(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.home_page = HomePage.objects.get()
        cls.page = BlogPostListPageFactory(parent=cls.home_page)

        BlogPostPageFactory(parent=cls.page)
        BlogPostPageFactory(parent=cls.page)

    def test_accessible(self) -> None:
        response = self.client.get(self.page.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["listing_pages"]), 2)
        self.assertContains(response, self.page.reverse_subpage("feed"))

    def test_queries(self) -> None:
        with self.assertNumQueries(44):
            self.client.get(self.page.url)

    def test_feed_accessible(self) -> None:
        with self.assertNumQueries(12):
            response = self.client.get(
                self.page.url + self.page.reverse_subpage("feed")
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/rss+xml; charset=utf-8")
