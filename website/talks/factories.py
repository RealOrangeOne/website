from datetime import timedelta

from website.common.factories import BaseContentFactory, BaseListingFactory

from . import models


class TalksListPageFactory(BaseListingFactory):
    class Meta:
        model = models.TalksListPage


class TalkPageFactory(BaseContentFactory):
    duration = timedelta(minutes=30)

    class Meta:
        model = models.TalkPage
