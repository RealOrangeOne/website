from django.conf import settings
from django.test import SimpleTestCase
from wagtail.rich_text import features as richtext_feature_registry

from website.common.embed import YouTubeLiteEmbedFinder
from website.common.utils import (
    count_words,
    extract_text,
    get_table_of_contents,
    heading_id,
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


class TableOfContentsTestCase(SimpleTestCase):
    def test_creates_table_of_contents(self) -> None:
        toc = get_table_of_contents(
            """
        <h2>2</h2>
        <h3>2.1</h3>
        <h3>2.2</h3>
        <h4>2.2.1</h4>
        <h3>2.3</h3>
        <h2>3</h2>
        <h3>3.1</h3>
        <h2>4</h2>
        """
        )

        self.assertEqual(len(toc), 3)
        self.assertEqual([entry.title for entry in toc], ["2", "3", "4"])
        self.assertEqual([entry.slug for entry in toc], ["ref-2", "ref-3", "ref-4"])

        first_entry = toc[0]
        self.assertEqual(len(first_entry.children), 3)
        self.assertEqual(
            [entry.title for entry in first_entry.children], ["2.1", "2.2", "2.3"]
        )

        sub_entry = first_entry.children[1]
        self.assertEqual(len(sub_entry.children), 1)
        self.assertEqual([entry.title for entry in sub_entry.children], ["2.2.1"])

        second_entry = toc[1]
        self.assertEqual(len(second_entry.children), 1)
        self.assertEqual([entry.title for entry in second_entry.children], ["3.1"])

    def test_no_headings(self) -> None:
        toc = get_table_of_contents("<p>I'm no heading</p>")
        self.assertEqual(toc, [])

    def test_no_content(self) -> None:
        toc = get_table_of_contents("")
        self.assertEqual(toc, [])

    def test_non_sequential_headings(self) -> None:
        toc = get_table_of_contents(
            """
        <h2>2</h2>
        <p>2 content</p>
        <h3>2.1</h3>
        <h3>2.2</h3>
        <p>2.2 content</p>
        <h5>2.2.1</h5>
        <h3>2.3</h3>
        """
        )

        self.assertEqual(len(toc), 1)

        first_entry = toc[0]
        self.assertEqual(len(first_entry.children), 3)
        self.assertEqual(
            [entry.title for entry in first_entry.children], ["2.1", "2.2", "2.3"]
        )
        self.assertEqual(
            [entry.slug for entry in first_entry.children],
            ["ref-21", "ref-22", "ref-23"],
        )

        sub_entry = first_entry.children[1]
        self.assertEqual(len(sub_entry.children), 1)
        self.assertEqual([entry.title for entry in sub_entry.children], ["2.2.1"])


class ExtractTextTestCase(SimpleTestCase):
    def test_extracts_text(self) -> None:
        self.assertEqual(extract_text("<p><b>Hello</b> there!</p>"), "Hello there!")
        self.assertEqual(
            extract_text("<p>Paragraph 1</p>\n<p>Paragraph 2</p>"),
            "Paragraph 1 Paragraph 2",
        )

    def test_plain_text(self) -> None:
        self.assertEqual(extract_text("Hello there!"), "Hello there!")


class CountWordsTestCase(SimpleTestCase):
    def test_counts_words(self) -> None:
        self.assertEqual(count_words("a b c"), 3)
        self.assertEqual(count_words("Correct Horse Battery Staple"), 4)
        self.assertEqual(count_words("Hello there! How are you?"), 5)


class RichTextFeaturesTestCase(SimpleTestCase):
    def test_features_exist(self) -> None:
        for editor, editor_config in settings.WAGTAILADMIN_RICH_TEXT_EDITORS.items():
            for feature in editor_config["OPTIONS"]["features"]:
                with self.subTest(editor=editor, feature=feature):
                    self.assertIsNotNone(
                        richtext_feature_registry.get_editor_plugin("draftail", feature)
                    )


class HeadingIDTestCase(SimpleTestCase):
    def test_headings(self) -> None:
        self.assertEqual(heading_id("123"), "ref-123")
        self.assertEqual(heading_id("test"), "test")
        self.assertEqual(heading_id("Look, a title!"), "look-a-title")
