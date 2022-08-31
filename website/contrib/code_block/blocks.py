from typing import Iterator

from django.utils.safestring import mark_safe
from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers import get_all_lexers, get_lexer_by_name
from wagtail.blocks import (
    BooleanBlock,
    CharBlock,
    ChoiceBlock,
    StructBlock,
    StructValue,
    TextBlock,
)


def get_language_choices() -> Iterator[tuple[str, str]]:
    for name, _, _, _ in sorted(get_all_lexers()):
        yield (name, name.replace("+", " + "))


class CodeStructValue(StructValue):
    def code(self) -> str:
        lexer = get_lexer_by_name(self.get("language"))
        formatter = HtmlFormatter(
            linenos=None,
        )
        return mark_safe(highlight(self.get("source"), lexer, formatter))


class CodeBlock(StructBlock):
    filename = CharBlock(max_length=128, required=False)
    language = ChoiceBlock(
        choices=get_language_choices,
    )
    source = TextBlock()
    always_show_header = BooleanBlock(default=False)

    class Meta:
        icon = "code"
        value_class = CodeStructValue
        template = "contrib/blocks/code.html"
