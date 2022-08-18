from django.template.loader import get_template
from django.test import SimpleTestCase, TestCase

from website.common.factories import ContentPageFactory, ListingPageFactory
from website.common.models import BasePage
from website.common.utils import get_page_models
from website.home.models import HomePage


class BasePageTestCase(SimpleTestCase):
    def test_unique_body_classes(self) -> None:
        body_classes = [page.body_class for page in get_page_models()]
        self.assertEqual(len(body_classes), len(set(body_classes)))

    def test_pages_inherit_base_page(self) -> None:
        for page_model in get_page_models():
            self.assertTrue(
                issubclass(page_model, BasePage),
                f"{page_model} does not inherit from {BasePage}.",
            )

    def test_pages_have_template(self) -> None:
        for page in get_page_models():
            get_template(page.template)


class ContentPageTestCase(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.home_page = HomePage.objects.get()
        cls.page = ContentPageFactory(parent=cls.home_page)

    def test_accessible(self) -> None:
        response = self.client.get(self.page.url)
        self.assertEqual(response.status_code, 200)

    def test_queries(self) -> None:
        with self.assertNumQueries(15):
            self.client.get(self.page.url)


class ListingPageTestCase(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.home_page = HomePage.objects.get()
        cls.page = ListingPageFactory(parent=cls.home_page)

        # Orphaned content page, shouldn't show up on lists
        ContentPageFactory()

        ContentPageFactory(parent=cls.page)
        ContentPageFactory(parent=cls.page)

    def test_accessible(self) -> None:
        response = self.client.get(self.page.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["child_pages"]), 2)

    def test_queries(self) -> None:
        expected_queries = 18

        with self.assertNumQueries(expected_queries):
            self.client.get(self.page.url)

        # Add another page, and check queries don't change
        ContentPageFactory(parent=self.page)

        with self.assertNumQueries(expected_queries):
            self.client.get(self.page.url)