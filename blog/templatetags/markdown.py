from django import template
from django.utils.safestring import mark_safe
import markdown2
import re

register = template.Library()

@register.filter(is_safe=True, name='markdown')
def markdown(text):
    # Parse youtube tags
    markup = ('''<div class="youtube-container">'''
            '''<iframe width="692" height="519" src="//www.youtube.com/embed/%s" frameborder="0" allowfullscreen></iframe>'''
        '''</div>''')
    regex = re.compile('\[youtube\:(.*)\]')

    def replacement(match):
        youtube_id = match.group(1)
        ytcontainer = markup % youtube_id
        return ytcontainer

    text = regex.sub(replacement, text);

    # Parse markdown
    text = mark_safe(markdown2.markdown(text))
    return text