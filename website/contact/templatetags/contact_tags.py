from django.template import Library
from django.utils.html import format_html

from website.contact.models import OnlineAccount

register = Library()


@register.simple_tag()
def mastodon_link() -> str:
    mastodon_account = OnlineAccount.objects.filter(name__iexact="mastodon").first()

    if mastodon_account is None:
        return ""

    return format_html('<link rel="me" href="{}" />', mastodon_account.url)
