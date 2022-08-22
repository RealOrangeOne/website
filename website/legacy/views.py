from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import RedirectView

from website.blog.models import BlogPostListPage


@method_decorator(cache_page(60 * 60), name="dispatch")
class PostsFeedView(RedirectView):
    def get_redirect_url(self) -> str:
        post_list = get_object_or_404(BlogPostListPage.objects.live())
        return post_list.url + post_list.reverse_subpage("feed")
