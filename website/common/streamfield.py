from itertools import product

from bs4 import BeautifulSoup, SoupStrainer
from django.utils import lorem_ipsum
from django.utils.html import format_html_join
from wagtail import blocks
from wagtail.contrib.typed_table_block.blocks import TypedTableBlock
from wagtail.embeds.blocks import EmbedBlock
from wagtail.images.blocks import ImageChooserBlock

from website.common.utils import HEADER_TAGS, heading_id
from website.contrib.code_block.blocks import CodeBlock
from website.contrib.mermaid_block.blocks import MermaidBlock


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
    caption = blocks.RichTextBlock(editor="plain", required=False)

    class Meta:
        icon = "image"
        label = "Image with caption"
        template = "common/blocks/image-caption.html"


class TangentBlock(blocks.StructBlock):
    name = blocks.CharBlock(max_length=64)
    content = blocks.RichTextBlock(editor="simple")

    class Meta:
        icon = "comment"
        label = "Tangent"
        template = "common/blocks/tangent.html"


class IFrameBlock(blocks.StructBlock):
    url = blocks.URLBlock()
    caption = blocks.RichTextBlock(editor="plain", required=False)

    class Meta:
        icon = "link-external"
        label = "IFrame"
        template = "common/blocks/iframe.html"


IGNORE_PLAINTEXT_BLOCKS = (
    blocks.RawHTMLBlock,
    EmbedBlock,
    ImageCaptionBlock,
    CodeBlock,
)
IGNORE_HEADING_BLOCKS = (*IGNORE_PLAINTEXT_BLOCKS, LoremBlock)


def get_blocks() -> list[tuple[str, blocks.BaseBlock]]:
    return [
        ("embed", EmbedBlock()),
        ("rich_text", blocks.RichTextBlock()),
        ("lorem", LoremBlock()),
        ("html", blocks.RawHTMLBlock()),
        ("image", ImageCaptionBlock()),
        ("code", CodeBlock()),
        ("tangent", TangentBlock()),
        ("mermaid", MermaidBlock()),
        (
            "table",
            TypedTableBlock(
                [
                    (
                        "rich_text",
                        blocks.RichTextBlock(editor="plain"),
                    ),
                    ("numeric", blocks.FloatBlock()),
                    ("text", blocks.CharBlock()),
                ]
            ),
        ),
        ("iframe", IFrameBlock()),
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
        slug = heading_id(tag.text)
        anchor = soup.new_tag("a", href="#" + slug, id=slug)
        anchor.string = "#"
        anchor.attrs["class"] = "heading-anchor"
        tag.insert(0, anchor)
    return str(soup)
