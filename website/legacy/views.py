from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_control
from django.views.generic import RedirectView

from website.blog.models import BlogPostListPage


@method_decorator(cache_control(max_age=60 * 60), name="dispatch")
class PostsFeedView(RedirectView):
    def get_redirect_url(self) -> str:
        post_list = get_object_or_404(BlogPostListPage)
        return post_list.url + post_list.reverse_subpage("feed")


@method_decorator(cache_control(max_age=60 * 60), name="dispatch")
class AllPagesFeedView(RedirectView):
    pattern_name = "feed"
