from django import template
from django.utils.safestring import mark_safe
import markdown2
import re

register = template.Library()

@register.filter(is_safe=True, name='markdown')
def markdown(text):
    # Parse youtube tags
    youtube_video_markup = ('''<div class="youtube-container">'''
            '''<iframe width="692" height="519" src="//www.youtube.com/embed/%s" frameborder="0" allowfullscreen></iframe>'''
        '''</div>''')
    regex = re.compile('\[youtube\:(.*)\]')

    def youtube_video_replacement(match):
        youtube_id = match.group(1)
        ytcontainer = youtube_video_markup % youtube_id
        return ytcontainer

    text = regex.sub(youtube_video_replacement, text);

    image_tag_extension_markup = ('''<img src="%s" alt="%s" class="%s"/>''')
    image_tag_extension_markup_with_title = ('''<img src="%s" alt="%s" class="%s" title="%s" />''')
    def image_tag_extension_replacement(match):
        alt_tag = match.group(1)
        class_tag = match.group(2)
        img_href = match.group(3)
        title_tag = match.group(5)

        if title_tag is not None:
            return image_tag_extension_markup_with_title % (img_href, alt_tag, class_tag, title_tag)
        else:
            return image_tag_extension_markup % (img_href, alt_tag, class_tag)

    # Parse own image tags
    regex = re.compile('\!\[(.*)\|(.*)\]\(([^ ]*)( ?"(.*)")?\)') # What a long ass regex...
    text = regex.sub(image_tag_extension_replacement, text)

    # Parse markdown
    text = mark_safe(markdown2.markdown(text))
    return text