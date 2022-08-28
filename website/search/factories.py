from website.common.factories import BaseContentFactory

from .models import SearchPage


class SearchPageFactory(BaseContentFactory):
    class Meta:
        model = SearchPage
