from rest_framework import serializers
from wagtail.models import Page


class PageLinkSerializer(serializers.ModelSerializer):
    full_url = serializers.SerializerMethodField()

    class Meta:
        model = Page
        fields = read_only_fields = ["full_url", "title"]

    def get_full_url(self, page: Page) -> str:
        return page.get_full_url(request=self.context["request"])
