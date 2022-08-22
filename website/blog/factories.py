from website.common.factories import BaseContentFactory

from . import models


class BlogPostListPageFactory(BaseContentFactory):
    class Meta:
        model = models.BlogPostListPage
