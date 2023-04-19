from typing import Iterator

from django.utils.safestring import mark_safe
from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers import find_lexer_class, get_all_lexers
from pygments.lexers.python import PythonConsoleLexer, PythonLexer
from pygments.lexers.special import TextLexer
from wagtail.blocks import CharBlock, ChoiceBlock, StructBlock, StructValue, TextBlock


def get_language_choices() -> Iterator[tuple[str, str]]:
    for name, _, _, _ in sorted(get_all_lexers()):
        yield (name, name.replace("+", " + "))


class CodeStructValue(StructValue):
    LANGUAGE_DISPLAY_MAPPING = {PythonConsoleLexer.name: PythonLexer.name}

    def code(self) -> str:
        lexer = find_lexer_class(self["language"])()
        formatter = HtmlFormatter(
            linenos=None,
        )
        return mark_safe(highlight(self["source"], lexer, formatter))

    def header_text(self) -> str:
        if filename := self["filename"]:
            return filename

        if self["language"] != TextLexer.name:
            return self.language_display()

        return ""

    def language_display(self) -> str:
        """
        Map ugly language names to something more useful
        """
        return self.LANGUAGE_DISPLAY_MAPPING.get(self["language"], self["language"])


class CodeBlock(StructBlock):
    filename = CharBlock(max_length=128, required=False)
    language = ChoiceBlock(
        choices=get_language_choices,
    )
    source = TextBlock()

    class Meta:
        icon = "code"
        value_class = CodeStructValue
        template = "contrib/blocks/code.html"
