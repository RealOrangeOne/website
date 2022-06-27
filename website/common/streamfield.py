from typing import Iterator

from django.utils import lorem_ipsum
from django.utils.html import format_html_join, strip_tags
from django.utils.text import smart_split
from wagtail import blocks
from wagtail.embeds.blocks import EmbedBlock

IGNORE_PLAINTEXT_BLOCKS = (blocks.RawHTMLBlock, EmbedBlock)

RICH_TEXT_FEATURES = [
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "bold",
    "italic",
    "ol",
    "ul",
    "link",
    "document-link",
    "code",
    "strikethrough",
]


class LoremBlock(blocks.StructBlock):
    paragraphs = blocks.IntegerBlock(min_value=1)

    def render(self, value: dict, context: dict | None = None) -> str:
        return format_html_join(
            "\n\n",
            "<p>{}</p>",
            [(paragraph,) for paragraph in lorem_ipsum.paragraphs(value["paragraphs"])],
        )

    class Meta:
        icon = "openquote"
        label = "Lorem Ipsum"


def get_blocks() -> list[tuple[str, blocks.BaseBlock]]:
    return [
        ("embed", EmbedBlock()),
        ("rich_text", blocks.RichTextBlock(features=RICH_TEXT_FEATURES)),
        ("lorem", LoremBlock()),
        ("html", blocks.RawHTMLBlock()),
    ]


def get_plain_text(value: blocks.StreamValue) -> Iterator[str]:
    for block in value:
        if isinstance(block.block_type, IGNORE_PLAINTEXT_BLOCKS):
            continue
        yield strip_tags(str(block))


def truncate_streamfield(value: blocks.StreamValue, words: int) -> str:
    collected_words: list[str] = []
    for block_text in get_plain_text(value):
        collected_words.extend(smart_split(block_text))
        if len(collected_words) >= words:
            break

    return " ".join(collected_words[:words])


def get_word_count(value: blocks.StreamValue) -> int:
    count = 0
    for chunk in get_plain_text(value):
        count += len(list(smart_split(chunk)))
    return count
