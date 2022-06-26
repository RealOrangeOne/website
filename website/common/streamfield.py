from django.utils import lorem_ipsum
from django.utils.html import format_html_join
from wagtail import blocks
from wagtail.embeds.blocks import EmbedBlock


class LoremBlock(blocks.StructBlock):
    paragraphs = blocks.IntegerBlock(min_value=1)

    def render(self, value: dict, context: dict) -> str:
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
        ("rich_text", blocks.RichTextBlock()),
        ("lorem", LoremBlock()),
        ("html", blocks.RawHTMLBlock()),
    ]
