from itertools import product
from typing import Iterable

from bs4 import BeautifulSoup
from django.utils import lorem_ipsum
from django.utils.html import format_html_join
from django.utils.text import slugify
from wagtail import blocks
from wagtail.embeds.blocks import EmbedBlock
from wagtail.images.blocks import ImageChooserBlock

from website.common.utils import HEADER_TAGS
from website.contrib.code_block.blocks import CodeBlock

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

RICH_TEXT_FEATURES_SIMPLE = [
    "bold",
    "italic",
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


class ImageCaptionBlock(blocks.StructBlock):
    image = ImageChooserBlock()
    caption = blocks.RichTextBlock(features=RICH_TEXT_FEATURES_SIMPLE)

    class Meta:
        icon = "image"
        label = "Image with caption"
        template = "common/blocks/image-caption.html"


IGNORE_PLAINTEXT_BLOCKS = (blocks.RawHTMLBlock, EmbedBlock, ImageCaptionBlock)
IGNORE_HEADING_BLOCKS = (*IGNORE_PLAINTEXT_BLOCKS, LoremBlock)


def get_blocks() -> list[tuple[str, blocks.BaseBlock]]:
    return [
        ("embed", EmbedBlock()),
        ("rich_text", blocks.RichTextBlock(features=RICH_TEXT_FEATURES)),
        ("lorem", LoremBlock()),
        ("html", blocks.RawHTMLBlock()),
        ("image", ImageCaptionBlock()),
        ("code", CodeBlock()),
    ]


def get_content_blocks(value: blocks.StreamValue) -> Iterable[blocks.BaseBlock]:
    for block in value:
        if not isinstance(block.block_type, IGNORE_PLAINTEXT_BLOCKS):
            yield block


def get_content_html(value: blocks.StreamValue) -> str:
    """
    Get the HTML of just original content (eg not embeds etc)
    """
    html = ""
    for block in get_content_blocks(value):
        html += str(block)
    return html


def add_heading_anchors(html: str) -> str:
    targets: list[str] = [
        f".block-{block_name} {header_tag}"
        for header_tag, block_name in product(
            HEADER_TAGS,
            [b[0] for b in get_blocks() if not isinstance(b[1], IGNORE_HEADING_BLOCKS)],
        )
    ]

    soup = BeautifulSoup(html, "lxml")
    for tag in soup.select(", ".join(targets)):
        slug = slugify(tag.text)
        anchor = soup.new_tag("a", href="#" + slug, id=slug)
        anchor.string = "#"
        anchor.attrs["class"] = "heading-anchor"
        tag.insert(0, anchor)
    return str(soup)
