import factory
import wagtail_factories

from . import models


class BaseContentFactory(wagtail_factories.PageFactory):
    title = factory.Faker("catch_phrase")
    subtitle = factory.Faker("bs")


class ContentPageFactory(BaseContentFactory):
    class Meta:
        model = models.ContentPage


class ListingPageFactory(BaseContentFactory):
    class Meta:
        model = models.ListingPage
