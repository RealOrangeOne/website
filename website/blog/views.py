from datetime import datetime, time

from website.common.views import ContentPageFeed

from .models import BlogPostPage


class BlogPostPageFeed(ContentPageFeed):
    def item_pubdate(self, item: BlogPostPage) -> datetime:
        return datetime.combine(item.date, time())
