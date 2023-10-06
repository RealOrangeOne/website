from bs4 import BeautifulSoup
from django.test import TestCase

from website.common.factories import ContentPageFactory
from website.home.models import HomePage

from .factories import SearchPageFactory
from .models import SearchPage


class SearchPageTestCase(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.home_page = HomePage.objects.get()
        cls.page = SearchPageFactory(parent=cls.home_page)

    def test_accessible(self) -> None:
        response = self.client.get(self.page.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["search_url"], "results/")
        self.assertEqual(response.context["MIN_SEARCH_LENGTH"], 3)

    def test_initial_query(self) -> None:
        response = self.client.get(self.page.url, {"q": "post 1"})
        self.assertEqual(response.context["search_query"], "post 1")
        self.assertTemplateNotUsed(response, "search/enter-search-term.html")

        search_input = BeautifulSoup(response.content, "lxml").find("input")
        self.assertEqual(search_input.attrs["value"], "post 1")

    def test_search_input(self) -> None:
        response = self.client.get(self.page.url)
        self.assertEqual(response.status_code, 200)

        soup = BeautifulSoup(response.content, "lxml")
        search_input = soup.find("input")

        self.assertEqual(search_input.attrs["name"], "q")
        self.assertEqual(search_input.attrs["hx-get"], "results/")
        self.assertEqual(search_input.attrs["value"], "")

        self.assertEqual(len(soup.select(search_input.attrs["hx-target"])), 1)
        self.assertEqual(len(soup.select(search_input.attrs["hx-indicator"])), 1)


class SearchPageResultsTestCase(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.home_page = HomePage.objects.get()
        cls.page = SearchPageFactory(parent=cls.home_page)

        for i in range(SearchPage.PAGE_SIZE + 1):
            ContentPageFactory(parent=cls.home_page, title=f"Post {i}")

        cls.url = cls.page.url + cls.page.reverse_subpage("results")

    def test_returns_results(self) -> None:
        with self.assertNumQueries(12):
            response = self.client.get(self.url, {"q": "post"}, HTTP_HX_REQUEST="true")
        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(response.context["results"]), SearchPage.PAGE_SIZE)
        self.assertEqual(response.context["paginator"].count, SearchPage.PAGE_SIZE + 1)
        self.assertEqual(response.context["search_query"], "post")
        self.assertEqual(response.context["page_num"], 1)

    def test_page_trigger(self) -> None:
        response = self.client.get(self.url, {"q": "post"}, HTTP_HX_REQUEST="true")
        self.assertEqual(response.status_code, 200)
        trigger = BeautifulSoup(response.content, "lxml").find(
            "span", attrs={"hx-trigger": "revealed"}
        )
        self.assertEqual(trigger.attrs["hx-swap"], "outerHTML")
        self.assertEqual(trigger.attrs["hx-get"], "results/?q=post&page=2")

    def test_pagination(self) -> None:
        response = self.client.get(
            self.url, {"q": "post", "page": 2}, HTTP_HX_REQUEST="true"
        )
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.context["page_num"], 2)
        self.assertEqual(len(response.context["results"]), 1)

        self.assertIsNone(
            BeautifulSoup(response.content, "lxml").find(
                "span", attrs={"hx-trigger": "revealed"}
            )
        )

    def test_too_high_page(self) -> None:
        with self.assertNumQueries(49):
            response = self.client.get(
                self.url, {"q": "post", "page": 30}, HTTP_HX_REQUEST="true"
            )
        self.assertEqual(response.status_code, 404)

    def test_returns_result(self) -> None:
        response = self.client.get(self.url, {"q": "post 1"}, HTTP_HX_REQUEST="true")
        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(response.context["results"]), 1)
        self.assertEqual(list(response.context["results"])[0].title, "Post 1")

    def test_no_results(self) -> None:
        response = self.client.get(self.url, {"q": "nothing"}, HTTP_HX_REQUEST="true")
        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(response.context["results"]), 0)
        self.assertContains(response, "No results found")

    def test_no_query(self) -> None:
        with self.assertNumQueries(7):
            response = self.client.get(self.url, HTTP_HX_REQUEST="true")
        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, "search/enter-search-term.html")

    def test_empty_query(self) -> None:
        with self.assertNumQueries(7):
            response = self.client.get(self.url, {"q": ""}, HTTP_HX_REQUEST="true")
        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, "search/enter-search-term.html")

    def test_not_htmx(self) -> None:
        with self.assertNumQueries(7):
            response = self.client.get(self.url)
        self.assertEqual(response.status_code, 400)
