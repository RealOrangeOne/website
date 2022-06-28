from django.test import SimpleTestCase

from .embed import YouTubeLiteEmbedFinder
from .models import BasePage
from .utils import get_page_models


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


class YouTubeLiteEmbedFinderTestCase(SimpleTestCase):
    def test_finds_video_id(self) -> None:
        self.assertEqual(
            YouTubeLiteEmbedFinder._get_video_id(
                '<iframe width="200" height="113" src="https://www.youtube.com/embed/dQw4w9WgXcQ?feature=oembed" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen title=""></iframe>'
            ),
            "dQw4w9WgXcQ",
        )
        with self.assertRaises(ValueError):
            YouTubeLiteEmbedFinder._get_video_id("something-else")
