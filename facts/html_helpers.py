import re

_tag_re = re.compile("<.*?>")


def remove_tags(raw_html):
    clean_text = re.sub(_tag_re, " ", raw_html)
    return clean_text
