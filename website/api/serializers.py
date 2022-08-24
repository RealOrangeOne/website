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

    def get_image(self, page: BlogPostPage) -> str:
        hero_image_url = page.hero_image_url

        if isinstance(hero_image_url, str) and hero_image_url[0] == "/":
            return self.context["request"].build_absolute_uri(hero_image_url)

        return hero_image_url
