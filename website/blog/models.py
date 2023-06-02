from typing import Any, Optional, Type

from django.contrib.postgres.search import TrigramSimilarity
from django.db import models
from django.db.models.functions import Cast
from django.utils import timezone
from django.utils.functional import cached_property
from modelcluster.fields import ParentalManyToManyField
from wagtail.admin.panels import FieldPanel
from wagtail.search import index
from wagtailautocomplete.edit_handlers import AutocompletePanel

from website.common.models import BaseContentPage, BaseListingPage
from website.common.utils import TocEntry
from website.common.views import ContentPageFeed
from website.contrib.singleton_page.utils import SingletonPageCache


class BlogPostListPage(BaseListingPage):
    max_count = 1
    subpage_types = [
        "blog.BlogPostPage",
        "blog.BlogPostTagListPage",
        "blog.BlogPostCollectionListPage",
        "blog.BlogPostCollectionPage",
    ]

    @cached_property
    def show_table_of_contents(self) -> bool:
        return False

    def get_listing_pages(self) -> models.QuerySet:
        return (
            BlogPostPage.objects.descendant_of(self)
            .live()
            .public()
            .order_by("-date", "title")
        )

    @property
    def feed_class(self) -> Type[ContentPageFeed]:
        from .views import BlogPostPageFeed

        return BlogPostPageFeed

    @cached_property
    def tag_list_page_url(self) -> Optional[str]:
        return SingletonPageCache.get_url(BlogPostTagListPage)


class BlogPostPage(BaseContentPage):
    subpage_types: list[Any] = []
    parent_page_types = [BlogPostListPage, "blog.BlogPostCollectionPage"]

    tags = ParentalManyToManyField("blog.BlogPostTagPage", blank=True)
    date = models.DateField(default=timezone.now)

    promote_panels = BaseContentPage.promote_panels + [
        FieldPanel("date"),
        AutocompletePanel("tags"),
    ]

    search_fields = BaseContentPage.search_fields + [
        index.RelatedFields("tags", [index.SearchField("title", boost=1)])
    ]

    @cached_property
    def tag_list_page_url(self) -> Optional[str]:
        return SingletonPageCache.get_url(BlogPostTagListPage)

    def get_similar_posts(self) -> models.QuerySet:
        try:
            listing_pages = BlogPostListPage.objects.get().get_listing_pages()
        except BlogPostListPage.DoesNotExist:
            return BlogPostPage.objects.none()

        similar_posts = listing_pages.exclude(id=self.id).alias(
            title_similarity=TrigramSimilarity("title", self.title),
            # If this page has no subtitle, ignore it as part of similarity
            subtitle_similarity=TrigramSimilarity("subtitle", self.subtitle)
            if self.subtitle
            else models.Value(1),
        )

        page_tags = list(self.tags.values_list("id", flat=True))
        similar_posts = similar_posts.alias(
            # If this page has no tags, ignore it as part of similarity
            # NB: Cast to a float, because `COUNT` returns a `bigint`.
            tag_similarity=Cast(
                models.Count("tags", filter=models.Q(tags__in=page_tags)),
                output_field=models.FloatField(),
            )
            / len(page_tags)
            if page_tags
            else models.Value(1)
        )

        similar_posts = similar_posts.annotate(
            similarity=(models.F("tag_similarity") * 2)
            * (models.F("title_similarity") * 10)
            * (models.F("subtitle_similarity"))
        ).order_by("-similarity")[:3]

        return similar_posts


class BlogPostTagListPage(BaseListingPage):
    max_count = 1
    parent_page_types = [BlogPostListPage]
    subpage_types = ["blog.BlogPostTagPage"]

    @cached_property
    def table_of_contents(self) -> list[TocEntry]:
        return [
            TocEntry(page.title, page.slug, 0, []) for page in self.get_listing_pages()
        ]


class BlogPostTagPage(BaseListingPage):
    subpage_types: list[Any] = []
    parent_page_types = [BlogPostTagListPage]

    @cached_property
    def html_title(self) -> str:
        return f"Pages tagged with '{super().html_title}'"

    def get_listing_pages(self) -> models.QuerySet:
        blog_list_page = BlogPostListPage.objects.get()
        return blog_list_page.get_listing_pages().filter(tags=self)

    @property
    def feed_class(self) -> Type[ContentPageFeed]:
        from .views import BlogPostPageFeed

        return BlogPostPageFeed


class BlogPostCollectionListPage(BaseListingPage):
    subpage_types: list[Any] = []
    parent_page_types = [BlogPostListPage]
    max_count = 1

    @cached_property
    def table_of_contents(self) -> list[TocEntry]:
        return [
            TocEntry(page.title, page.slug, 0, []) for page in self.get_listing_pages()
        ]

    def get_listing_pages(self) -> models.QuerySet:
        blog_list_page = BlogPostListPage.objects.get()
        return BlogPostCollectionPage.objects.child_of(blog_list_page).live().public()


class BlogPostCollectionPage(BaseListingPage):
    parent_page_types = [BlogPostListPage]
    subpage_types = [BlogPostPage]

    def get_listing_pages(self) -> models.QuerySet:
        return (
            BlogPostPage.objects.child_of(self)
            .live()
            .public()
            .order_by("-date", "title")
        )

    @property
    def feed_class(self) -> Type[ContentPageFeed]:
        from .views import BlogPostPageFeed

        return BlogPostPageFeed
