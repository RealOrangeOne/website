from typing import Iterator

from django.utils.functional import cached_property
from django.utils.safestring import mark_safe
from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers import find_lexer_class, get_all_lexers
from pygments.lexers.python import PythonConsoleLexer, PythonLexer
from pygments.lexers.shell import BashLexer, BashSessionLexer
from pygments.lexers.special import TextLexer
from pygments.lexers.sql import PostgresConsoleLexer, PostgresLexer
from wagtail.blocks import CharBlock, ChoiceBlock, StructBlock, StructValue, TextBlock

from .utils import get_linguist_colours


def get_language_choices() -> Iterator[tuple[str, str]]:
    for name, _, _, _ in sorted(get_all_lexers()):
        yield (name, name.replace("+", " + "))


class CodeStructValue(StructValue):
    LANGUAGE_DISPLAY_MAPPING = {
        PythonConsoleLexer.name: PythonLexer.name,
        PostgresLexer.name: "PostgreSQL",
    }

    LINGUIST_MAPPING = {
        BashLexer.name: "Shell",
        BashSessionLexer.name: "Shell",
        PostgresLexer.name: "PLpgSQL",
        PostgresConsoleLexer.name: "PLpgSQL",
    }

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

    @cached_property
    def colour(self) -> str | None:
        """
        Expose the colour denoted by GitHub's linguist.
        """
        linguist_colours = get_linguist_colours()

        language = self.LINGUIST_MAPPING.get(self["language"], self["language"])

        if exact_match := linguist_colours.get(language.lower()):
            return exact_match

        if language_display_match := linguist_colours.get(
            self.LANGUAGE_DISPLAY_MAPPING.get(language, "").lower()
        ):
            return language_display_match

        return None


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
