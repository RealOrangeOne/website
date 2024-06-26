from bs4 import BeautifulSoup
from django.test import TestCase
from django.urls import reverse

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
        self.assertNotIn("value", search_input.attrs)  # Because of minify-html

        self.assertEqual(len(soup.select(search_input.attrs["hx-target"])), 1)
        self.assertEqual(len(soup.select(search_input.attrs["hx-indicator"])), 2)


class SearchPageResultsTestCase(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.home_page = HomePage.objects.get()
        cls.page = SearchPageFactory(parent=cls.home_page)

        for i in range(SearchPage.PAGE_SIZE + 1):
            ContentPageFactory(parent=cls.home_page, title=f"Post {i}")

        cls.url = cls.page.url + cls.page.reverse_subpage("results")

    def test_returns_results(self) -> None:
        with self.assertNumQueries(23):
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
        with self.assertNumQueries(42):
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
        with self.assertNumQueries(6):
            response = self.client.get(self.url, HTTP_HX_REQUEST="true")
        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, "search/enter-search-term.html")

    def test_empty_query(self) -> None:
        with self.assertNumQueries(6):
            response = self.client.get(self.url, {"q": ""}, HTTP_HX_REQUEST="true")
        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, "search/enter-search-term.html")

    def test_not_htmx(self) -> None:
        with self.assertNumQueries(6):
            response = self.client.get(self.url)
        self.assertEqual(response.status_code, 400)


class OpenSearchTestCase(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.home_page = HomePage.objects.get()
        cls.page = SearchPageFactory(parent=cls.home_page)

        for i in range(6):
            ContentPageFactory(parent=cls.home_page, title=f"Post {i}")

    def test_opensearch_description(self) -> None:
        with self.assertNumQueries(6):
            response = self.client.get(reverse("opensearch"))
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, reverse("go"))
        self.assertContains(response, reverse("opensearch-suggestions"))

    def test_opensearch_suggestions(self) -> None:
        with self.assertNumQueries(3):
            response = self.client.get(reverse("opensearch-suggestions"), {"q": "post"})
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertEqual(data[0], "post")
        self.assertEqual(data[1], [f"Post {i}" for i in range(5)])


class GoViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.home_page = HomePage.objects.get()
        cls.search_page = SearchPageFactory(parent=cls.home_page)

        cls.post_1 = ContentPageFactory(
            parent=cls.home_page, title="Post Title 1", slug="post-slug-1"
        )
        cls.post_2 = ContentPageFactory(
            parent=cls.home_page, title="Post Title 2", slug="post-slug-2"
        )

    def test_by_title(self) -> None:
        with self.assertNumQueries(5):
            response = self.client.get(reverse("go"), {"q": self.post_1.title})

        self.assertRedirects(
            response, self.post_1.get_url(), fetch_redirect_response=True
        )

    def test_by_slug(self) -> None:
        with self.assertNumQueries(6):
            response = self.client.get(reverse("go"), {"q": self.post_2.slug})

        self.assertRedirects(
            response, self.post_2.get_url(), fetch_redirect_response=True
        )

    def test_no_match(self) -> None:
        with self.assertNumQueries(6):
            response = self.client.get(reverse("go"), {"q": "Something else"})

        self.assertRedirects(
            response,
            self.search_page.get_url() + "?q=Something+else",
            fetch_redirect_response=True,
        )

    def test_no_query(self) -> None:
        with self.assertNumQueries(3):
            response = self.client.get(reverse("go"))

        self.assertRedirects(
            response, self.search_page.get_url(), fetch_redirect_response=True
        )

    def test_multiple_matches(self) -> None:
        ContentPageFactory(parent=self.home_page, title=self.post_1.title)

        with self.assertNumQueries(6):
            response = self.client.get(reverse("go"), {"q": self.post_1.title})

        self.assertRedirects(
            response,
            self.search_page.get_url() + f"?q={self.post_1.title}",
            fetch_redirect_response=True,
        )

    def test_no_search_page(self) -> None:
        self.search_page.delete()

        response = self.client.get(reverse("go"))

        self.assertEqual(response.status_code, 404)
