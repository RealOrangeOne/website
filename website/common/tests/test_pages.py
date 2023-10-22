from django.template.loader import get_template
from django.test import SimpleTestCase, TestCase

from website.common.factories import ContentPageFactory, ListingPageFactory
from website.common.models import BaseListingPage, BasePage
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
        with self.assertNumQueries(39):
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
        with self.assertNumQueries(42):
            response = self.client.get(self.page.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["listing_pages"]), 2)
        self.assertContains(response, self.page.reverse_subpage("feed"))

    def test_feed_accessible(self) -> None:
        with self.assertNumQueries(13):
            response = self.client.get(
                self.page.url + self.page.reverse_subpage("feed")
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/xml")
        self.assertContains(response, "xml-stylesheet")

    def test_meta_url(self) -> None:
        response = self.client.get(self.page.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["page"].get_meta_url(), self.page.full_url)

    def test_meta_url_with_page(self) -> None:
        ContentPageFactory.create_batch(BaseListingPage.PAGE_SIZE, parent=self.page)
        response = self.client.get(self.page.url, {"page": 2})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context["page"].get_meta_url(), self.page.full_url + "?page=2"
        )
