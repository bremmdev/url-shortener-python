import re

def is_valid_url(url):
    url_regex = re.compile(
        r'(?i)\b((?:https?|ftp)://(?:www\d?\.)?|www\d?\.)'
        r'(?:(?:[a-z0-9\-._~%!$&\'()*+,;=]|%[0-9a-f]{2})+/?|[a-z0-9\-._~%!$&\'()*+,;=]|%[0-9a-f]{2})+'
        r'(?:\?[\w\-._~%!$&\'()*+,;=:@/?]|#(?:[\w\-._~%!$&\'()*+,;=:@/?]|%[0-9a-f]{2}))*'
    )
    return url_regex.match(url)

def is_valid_custom_url(custom_url):
    # 4-12 characters, no special characters, only _ and - allowed
    custom_regex = re.compile(r'^[a-zA-Z0-9_-]{4,12}$')
    return custom_regex.match(custom_url)