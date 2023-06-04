import re

from django.test import SimpleTestCase
from django.urls import reverse

from .blocks import CodeStructValue, get_language_choices
from .utils import PYGMENTS_VERSION_SLUG, get_linguist_colours


class PygmentsStylesTestCase(SimpleTestCase):
    url = reverse("code-block:styles")

    def test_accessible(self) -> None:
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Cache-Control"], "max-age=3600")
        self.assertEqual(response["Content-Type"], "text/css")

    def test_url_contains_version(self) -> None:
        self.assertIn(PYGMENTS_VERSION_SLUG, self.url)


class CodeStructValueTestCase(SimpleTestCase):
    def test_highlights(self) -> None:
        for language, _ in get_language_choices():
            with self.subTest(language):
                block = CodeStructValue(
                    None, [("source", "test"), ("language", language)]
                )
                self.assertIsInstance(block.code(), str)

    def test_header_text_uses_filename(self) -> None:
        block = CodeStructValue(None, [("filename", "test.txt")])
        self.assertEqual(block.header_text(), "test.txt")

    def test_header_text_uses_language(self) -> None:
        block = CodeStructValue(None, [("filename", ""), ("language", "Python")])
        self.assertEqual(block.header_text(), "Python")

    def test_header_text_uses_language_mapping(self) -> None:
        block = CodeStructValue(
            None, [("filename", ""), ("language", "Python console session")]
        )
        self.assertEqual(block.header_text(), "Python")

    def test_header_text_empty_when_text(self) -> None:
        block = CodeStructValue(None, [("filename", ""), ("language", "Text only")])
        self.assertEqual(block.header_text(), "")

    def test_linguist_mapping(self) -> None:
        linguist_languages = set(get_linguist_colours().keys())

        for language in CodeStructValue.LINGUIST_MAPPING.values():
            self.assertIn(language.lower(), linguist_languages)


class LinguistColoursTestCase(SimpleTestCase):
    HEX_RE = re.compile(r"#[0-9A-F]", re.IGNORECASE)

    def test_gets_colours(self) -> None:
        colours = get_linguist_colours()

        for colour in colours.values():
            with self.subTest(colour):
                self.assertRegex(colour, self.HEX_RE)
