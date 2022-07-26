from django.utils.functional import cached_property

from website.common.models import BaseContentMixin, BasePage
from website.common.utils import TocEntry


class SearchPage(BaseContentMixin, BasePage):  # type: ignore[misc]
    max_count = 1
    subpage_types: list = []
    parent_page_types = ["home.HomePage"]
    content_panels = BasePage.content_panels + BaseContentMixin.content_panels

    @cached_property
    def reading_time(self) -> int:
        """
        How does one read a search page?
        """
        return 0

    @cached_property
    def table_of_contents(self) -> list[TocEntry]:
        return []
