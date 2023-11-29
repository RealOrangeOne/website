from typing import Any

from django.http import HttpRequest
from django.utils.feedgenerator import DefaultFeed
from django.utils.xmlutils import SimplerXMLGenerator


class CustomFeed(DefaultFeed):
    """
    A custom feed generator with additional features.
    """

    def __init__(self, request: HttpRequest, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.request = request

    def add_root_elements(self, handler: SimplerXMLGenerator) -> None:
        super().add_root_elements(handler)
        handler.startElement("image", {})
        handler.addQuickElement("url", self.request.build_absolute_uri("favicon.ico"))
        handler.addQuickElement("title", self.feed["title"])
        handler.addQuickElement("link", self.feed["link"])
        handler.endElement("image")
