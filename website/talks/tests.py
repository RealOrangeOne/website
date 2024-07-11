from django.test import TestCase
from django.urls import reverse

from website.home.models import HomePage

from .factories import TalkPageFactory, TalksListPageFactory


class TalkPageTestCase(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.home_page = HomePage.objects.get()
        cls.list_page = TalksListPageFactory(parent=cls.home_page)
        cls.page = TalkPageFactory(parent=cls.list_page)

    def test_accessible(self) -> None:
        response = self.client.get(self.page.url)
        self.assertEqual(response.status_code, 200)

    def test_queries(self) -> None:
        with self.assertNumQueries(34):
            self.client.get(self.page.url)


class TalksListPageTestCase(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.home_page = HomePage.objects.get()
        cls.page = TalksListPageFactory(parent=cls.home_page)

        TalkPageFactory(parent=cls.page)
        TalkPageFactory(parent=cls.page)

    def test_accessible(self) -> None:
        response = self.client.get(self.page.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["listing_pages"]), 2)

    def test_queries(self) -> None:
        with self.assertNumQueries(34):
            self.client.get(self.page.url)

    def test_feed_accessible(self) -> None:
        response = self.client.get(self.page.url + self.page.reverse_subpage("feed"))
        self.assertRedirects(
            response, reverse("feed"), status_code=301, fetch_redirect_response=True
        )
