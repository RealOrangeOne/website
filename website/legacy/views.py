from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_control
from django.views.generic import RedirectView

from website.blog.models import BlogPostTagListPage, BlogPostTagPage


@method_decorator(cache_control(max_age=60 * 60), name="dispatch")
class AllPagesFeedView(RedirectView):
    pattern_name = "feed"
    permanent = True


@method_decorator(cache_control(max_age=60 * 60), name="dispatch")
class TagView(RedirectView):
    permanent = True

    def get_redirect_url(self, slug: str) -> str:
        tag = get_object_or_404(BlogPostTagPage, slug=slug)
        return tag.get_url(request=self.request)


@method_decorator(cache_control(max_age=60 * 60), name="dispatch")
class TagsView(RedirectView):
    def get_redirect_url(self) -> str:
        tag_list = get_object_or_404(BlogPostTagListPage)
        return tag_list.get_url(request=self.request)
