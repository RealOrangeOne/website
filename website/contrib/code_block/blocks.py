from typing import Iterator

from django.utils.safestring import mark_safe
from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers import get_all_lexers, get_lexer_by_name
from wagtail.blocks import ChoiceBlock, StructBlock, StructValue, TextBlock


def get_language_choices() -> Iterator[tuple[str, str]]:
    for name, _, _, _ in sorted(get_all_lexers()):
        yield (name, name)


class CodeStructValue(StructValue):
    def code(self) -> str:
        lexer = get_lexer_by_name(self.get("language"))
        formatter = HtmlFormatter(
            linenos=None,
        )
        return mark_safe(highlight(self.get("source"), lexer, formatter))


class CodeBlock(StructBlock):
    language = ChoiceBlock(
        choices=get_language_choices,
    )
    source = TextBlock()

    class Meta:
        icon = "code"
        value_class = CodeStructValue
        template = "contrib/blocks/code.html"
