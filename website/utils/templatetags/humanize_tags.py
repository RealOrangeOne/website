import humanize
from django.template import Library

register = Library()

register.filter(humanize.naturaldelta)
