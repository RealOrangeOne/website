from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register

from .models import BlogPostTag


class BlogPostTagModelAdmin(ModelAdmin):
    model = BlogPostTag
    menu_label = "Blog Post Tags"
    menu_icon = "tag"
    list_display = ["name", "slug"]
    search_fields = ["name", "slug"]


modeladmin_register(BlogPostTagModelAdmin)
