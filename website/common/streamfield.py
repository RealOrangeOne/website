from itertools import product

from bs4 import BeautifulSoup, SoupStrainer
from django.utils import lorem_ipsum
from django.utils.html import format_html_join
from django.utils.text import slugify
from wagtail import blocks
from wagtail.embeds.blocks import EmbedBlock
from wagtail.images.blocks import ImageChooserBlock

from website.common.utils import HEADER_TAGS
from website.contrib.code_block.blocks import CodeBlock

RICH_TEXT_FEATURES = [
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

RICH_TEXT_FEATURES_PLAIN = [
    "bold",
    "italic",
    "link",
    "document-link",
    "code",
    "strikethrough",
]

RICH_TEXT_FEATURES_SIMPLE = [
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


class ImageCaptionBlock(blocks.StructBlock):
    image = ImageChooserBlock()
    caption = blocks.RichTextBlock(features=RICH_TEXT_FEATURES_PLAIN)

    class Meta:
        icon = "image"
        label = "Image with caption"
        template = "common/blocks/image-caption.html"


class TangentBlock(blocks.StructBlock):
    name = blocks.CharBlock(max_length=64)
    content = blocks.RichTextBlock(features=RICH_TEXT_FEATURES_SIMPLE)

    class Meta:
        icon = "comment"
        label = "Tangent"
        template = "common/blocks/tangent.html"


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
        ("tangent", TangentBlock()),
    ]


def get_content_html(html: str) -> str:
    """
    Get the HTML of just original content (eg not embeds etc)
    """
    block_classes = [
        f"block-{block_name}"
        for block_name, block in get_blocks()
        if not isinstance(block, IGNORE_PLAINTEXT_BLOCKS)
    ]

    return str(
        BeautifulSoup(html, "lxml", parse_only=SoupStrainer(class_=block_classes))
    )


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
