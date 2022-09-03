from rest_framework import serializers
from wagtail.models import Page

from website.blog.models import BlogPostPage


class PageLinkSerializer(serializers.ModelSerializer):
    full_url = serializers.SerializerMethodField()

    class Meta:
        model = Page
        fields = read_only_fields = ["full_url", "title"]

    def get_full_url(self, page: Page) -> str:
        return page.get_full_url(request=self.context["request"])


class LMOTFYSerializer(serializers.ModelSerializer):
    full_url = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    class Meta:
        model = BlogPostPage
        fields = read_only_fields = ["full_url", "title", "summary", "image", "date"]

    def get_full_url(self, page: BlogPostPage) -> str:
        return page.get_full_url(request=self.context["request"])

    def get_image(self, page: BlogPostPage) -> str | None:
        image_url = page.get_meta_image_url(request=self.context["request"])

        if not image_url:
            return None

        if image_url[0] == "/":
            return self.context["request"].build_absolute_uri(image_url)

        return image_url
