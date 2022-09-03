import base64
import json
import zlib

from wagtail.blocks import RichTextBlock, StructBlock, StructValue, TextBlock


class MermaidStructValue(StructValue):
    def config(self) -> dict:
        return {"code": self.get("source"), "mermaid": {"theme": "default"}}

    def pako(self) -> str:
        """
        Reverse engineer the URL payload needed by mermaid.ink
        """
        return (
            "pako:"
            + base64.urlsafe_b64encode(
                zlib.compress(json.dumps(self.config()).encode())
            ).decode()
        )


class MermaidBlock(StructBlock):
    source = TextBlock()
    caption = RichTextBlock(editor="plain", required=False)

    class Meta:
        icon = "edit"
        value_class = MermaidStructValue
        template = "contrib/blocks/mermaid.html"
