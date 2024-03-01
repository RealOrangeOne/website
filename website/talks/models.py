from datetime import timedelta
from typing import Any

from django.db import models
from django.utils import timezone
from wagtail.admin.panels import FieldPanel, MultiFieldPanel

from website.common.models import BaseContentPage, BaseListingPage


class TalksListPage(BaseListingPage):
    max_count = 1
    subpage_types = ["talks.TalkPage"]


class TalkPage(BaseContentPage):
    subpage_types: list[Any] = []
    parent_page_types = [TalksListPage]

    date = models.DateField(default=timezone.now)

    duration = models.DurationField()

    slides_url = models.URLField(blank=True)
    video_url = models.URLField(blank=True)

    content_panels = BaseContentPage.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("slides_url"),
                FieldPanel("video_url"),
            ],
            heading="Media",
        ),
        FieldPanel("duration"),
    ]

    promote_panels = BaseContentPage.promote_panels + [
        FieldPanel("date"),
    ]

    @property
    def show_table_of_contents(self) -> bool:
        return False

    @property
    def reading_time(self) -> timedelta:
        return self.duration

    @property
    def word_count(self) -> int:
        return 0
