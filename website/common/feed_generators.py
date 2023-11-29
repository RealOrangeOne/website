from django.utils.feedgenerator import DefaultFeed


class CustomFeed(DefaultFeed):
    """
    A custom feed generator with additional features.
    """

    def __init__(self, request, **kwargs):
        super().__init__(**kwargs)
        self.request = request

    def add_root_elements(self, handler) -> None:
        super().add_root_elements(handler)
        handler.startElement("image", {})
        handler.addQuickElement("url", self.request.build_absolute_uri("favicon.ico"))
        handler.addQuickElement("title", self.feed["title"])
        handler.addQuickElement("link", self.feed["link"])
        handler.endElement("image")
