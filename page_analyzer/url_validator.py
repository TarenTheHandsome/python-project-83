from urllib.parse import urlparse
from page_analyzer.database import get_all_urls


def normalize_url(url):
    return f'{urlparse(url).scheme}://{urlparse(url).hostname}'


def validator(url):
    errors = set()
    errors.add(bool(url))
    errors.add((bool(urlparse(url).scheme)))
    errors.add((bool(urlparse(url).netloc)))
    if len(url) > 255:
        errors.add(False)
    if False in errors:
        return True
    return False

def name_validator(url):
    errors = []
    url_name = normalize_url(url)
    all_urls = get_all_urls()
    for u in all_urls:
        if url_name == u['name']:
            errors.append(True)
    return errors

