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
        with self.assertNumQueries(48):
            self.client.get(self.page.url)


class BlogPostPageSimilarityTestCase(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.home_page = HomePage.objects.get()
        cls.blog_post_list_page = BlogPostListPageFactory(parent=cls.home_page)
        cls.page = BlogPostPageFactory(
            parent=cls.blog_post_list_page, title="Blog post 1"
        )

        cls.similar_page_1 = BlogPostPageFactory(
            parent=cls.blog_post_list_page, title="Blog post 2"
        )
        cls.similar_page_2 = BlogPostPageFactory(
            parent=cls.blog_post_list_page, title="Blog post 3"
        )
        cls.similar_page_3 = BlogPostPageFactory(
            parent=cls.blog_post_list_page, title="Blog post 4"
        )

        BlogPostPageFactory(parent=cls.blog_post_list_page, title="Legal documents")

    def test_similar_pages(self) -> None:
        self.assertEqual(
            set(self.page.get_similar_posts()),
            {self.similar_page_1, self.similar_page_2, self.similar_page_3},
        )

    def test_page_similarity(self) -> None:
        for page in self.page.get_similar_posts():
            self.assertNotEqual(page.similarity, 0.0)

    def test_ordered_by_similarity(self) -> None:
        similar_pages = self.page.get_similar_posts()
        self.assertEqual(
            list(similar_pages),
            sorted(similar_pages, key=lambda p: p.similarity, reverse=True),
        )


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
        self.assertEqual(response["Content-Type"], "application/xml")
        self.assertContains(response, "xml-stylesheet")
