import factory

from website.common.factories import BaseContentFactory, BaseListingFactory

from . import models


class BlogPostListPageFactory(BaseListingFactory):
    class Meta:
        model = models.BlogPostListPage


class BlogPostPageFactory(BaseContentFactory):
    class Meta:
        model = models.BlogPostPage


class ExternalBlogPostPageFactory(BaseContentFactory):
    external_url = factory.Faker("url")

    class Meta:
        model = models.ExternalBlogPostPage
        exclude = ["subtitle"]
