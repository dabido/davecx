from django import template
from django.utils.safestring import mark_safe
import re
register = template.Library()

def parse_urls(string):
	return re.sub(r"\[(.*)\|(.*)\]", r'<a target="_blank" href="\2">\1</a>', string)

@register.filter(needs_autoescape=False)
def parse_tags(string):
	# Tag for parsing custom tags
	result = parse_urls(string)
	return mark_safe(result)