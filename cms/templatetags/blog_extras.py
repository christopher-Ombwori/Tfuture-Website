from django import template
from django.utils.html import strip_tags

register = template.Library()


@register.filter
def reading_time(page):
    """Estimate reading time (minutes) from page title, intro and streamfield text blocks.
    Returns a string like '3 min read'."""
    if not page:
        return ''

    text_parts = []
    try:
        if getattr(page, 'title', None):
            text_parts.append(str(page.title))
        if getattr(page, 'intro', None):
            text_parts.append(strip_tags(str(page.intro)))
        # StreamField: iterate blocks and collect textual values
        body = getattr(page, 'body', None)
        if body:
            for block in body:
                try:
                    value = block.value
                    # If simple string-like
                    if isinstance(value, str):
                        text_parts.append(strip_tags(value))
                    # If StructBlock/Dict-like
                    elif isinstance(value, dict):
                        for v in value.values():
                            if isinstance(v, str):
                                text_parts.append(strip_tags(v))
                            else:
                                text_parts.append(strip_tags(str(v)))
                    else:
                        text_parts.append(strip_tags(str(value)))
                except Exception:
                    continue
    except Exception:
        return ''

    text = ' '.join(text_parts)
    words = len(text.split())
    minutes = max(1, int(round(words / 200.0)))
    return f"{minutes} min read"
