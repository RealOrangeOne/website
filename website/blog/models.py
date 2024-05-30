from typing import Any, Optional
from urllib.parse import urlsplit

from django.contrib.postgres.search import TrigramSimilarity
from django.db import models
from django.db.models.functions import Cast, Coalesce
from django.http import HttpRequest, HttpResponse, HttpResponsePermanentRedirect
from django.utils import timezone
from django.utils.functional import cached_property
from metadata_parser import MetadataParser
from modelcluster.fields import ParentalManyToManyField
from wagtail.admin.panels import FieldPanel
from wagtail.models import Page, PageQuerySet, Site
from wagtail.search import index
from wagtailautocomplete.edit_handlers import AutocompletePanel

from website.common.models import BaseContentPage, BaseListingPage, BasePage
from website.common.utils import (
    TocEntry,
    extend_query_params,
    get_page_metadata,
    get_url_mime_type,
)
from website.contrib.singleton_page.utils import SingletonPageCache


class BlogPostListPage(BaseListingPage):
    max_count = 1
    subpage_types = [
        "blog.BlogPostPage",
        "blog.BlogPostTagListPage",
        "blog.BlogPostCollectionListPage",
        "blog.BlogPostCollectionPage",
        "blog.BlogPostCollectionPage",
        "blog.ExternalBlogPostPage",
    ]

    @cached_property
    def show_table_of_contents(self) -> bool:
        return False

    def get_listing_pages(self) -> models.QuerySet:
        return (
            Page.objects.live()
            .public()
            .annotate(date=Coalesce("blogpostpage__date", "externalblogpostpage__date"))
            .descendant_of(self)
            .type(BlogPostPage, ExternalBlogPostPage)
            .specific()
            .order_by("-date", "title")
        )

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

    @cached_property
    def tags_list(self) -> models.QuerySet:
        """
        Use this to get a page's tags.
        """
        tags = self.tags.order_by("slug")

        # In drafts, `django-modelcluster` doesn't support these filters
        if isinstance(tags, PageQuerySet):
            return tags.public().live()

        return tags

    @cached_property
    def blog_post_list_page_url(self) -> Optional[str]:
        return SingletonPageCache.get_url(BlogPostListPage)

    def get_similar_posts(self) -> models.QuerySet:
        try:
            listing_pages = BlogPostPage.objects.filter(
                id__in=BlogPostListPage.objects.get().get_listing_pages()
            )
        except BlogPostListPage.DoesNotExist:
            return BlogPostPage.objects.none()

        similar_posts = listing_pages.exclude(id=self.id).alias(
            title_similarity=TrigramSimilarity("title", self.title),
        )

        page_tags = list(self.tags.public().live().values_list("id", flat=True))
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
            + (models.F("title_similarity") * 10)
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
        listing_pages = blog_list_page.get_listing_pages()
        blog_post_tags = list(
            BlogPostPage.objects.filter(id__in=listing_pages, tags=self).values_list(
                "id", flat=True
            )
        )
        external_post_tags = list(
            ExternalBlogPostPage.objects.filter(
                id__in=listing_pages, tags=self
            ).values_list("id", flat=True)
        )
        return listing_pages.filter(
            id__in=blog_post_tags + external_post_tags
        ).specific()


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


class ExternalBlogPostPage(BaseContentPage):
    subpage_types: list[Any] = []
    parent_page_types = [BlogPostListPage]
    preview_modes: list[Any] = []

    is_external = True

    # Some `BaseContentPage` fields aren't relevant
    body = None
    subtitle = None
    hero_image = None
    hero_unsplash_photo = None

    external_url = models.URLField()

    tags = ParentalManyToManyField("blog.BlogPostTagPage", blank=True)
    date = models.DateField(default=timezone.now)

    content_panels = BasePage.content_panels + [FieldPanel("external_url")]

    promote_panels = BaseContentPage.promote_panels + [
        FieldPanel("date"),
        AutocompletePanel("tags"),
    ]

    search_fields = BaseContentPage.search_fields + [
        index.RelatedFields("tags", [index.SearchField("title", boost=1)]),
        index.SearchField("external_url"),
    ]

    @cached_property
    def tag_list_page_url(self) -> Optional[str]:
        return SingletonPageCache.get_url(BlogPostTagListPage)

    @cached_property
    def tags_list(self) -> models.QuerySet:
        """
        Use this to get a page's tags.
        """
        tags = self.tags.order_by("slug")

        # In drafts, `django-modelcluster` doesn't support these filters
        if isinstance(tags, PageQuerySet):
            return tags.public().live()

        return tags

    @cached_property
    def metadata(self) -> MetadataParser:
        return get_page_metadata(self.external_url)

    @cached_property
    def _body_html(self) -> str:
        try:
            return self.metadata.get_metadatas("description")[0]
        except (KeyError, IndexError, TypeError):
            return ""

    @cached_property
    def plain_text(self) -> str:
        # The metadata is already just text
        return self._body_html

    def hero_url(
        self, image_size: str, wagtail_image_spec_extra: Optional[str] = None
    ) -> Optional[str]:
        try:
            return self.metadata.get_metadatas("image")[0]
        except (KeyError, IndexError, TypeError):
            return None

    @cached_property
    def hero_image_url(self) -> str:
        return ""

    @cached_property
    def hero_image_alt(self) -> str:
        return ""

    def get_meta_image_mime(self) -> Optional[str]:
        return get_url_mime_type(self.hero_url(""))

    def get_url(
        self, request: HttpRequest | None = None, current_site: Site | None = None
    ) -> str:
        return self.get_full_url(request)

    def get_full_url(self, request: HttpRequest | None = None) -> str:
        full_url = urlsplit(super().get_full_url(request))
        return extend_query_params(self.external_url, {"utm_source": full_url.netloc})

    def serve(self, request: HttpRequest, *args: tuple, **kwargs: dict) -> HttpResponse:
        """
        Send the user directly to the external page
        """
        return HttpResponsePermanentRedirect(self.get_full_url(request))
