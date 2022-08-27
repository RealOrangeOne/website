from website.common.factories import BaseContentFactory, BaseListingFactory

from . import models


class BlogPostListPageFactory(BaseListingFactory):
    class Meta:
        model = models.BlogPostListPage


class BlogPostPageFactory(BaseContentFactory):
    class Meta:
        model = models.BlogPostPage
