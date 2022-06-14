from django.template import Library

from website.home.models import HomePage

register = Library()


@register.inclusion_tag("common/footer.html")
def footer() -> dict:
    return {
        "homepage": HomePage.objects.live().get(),
    }
