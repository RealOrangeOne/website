from django.template import Library

register = Library()


@register.filter(name="range")
def do_range(stop: int) -> range:
    return range(stop)
