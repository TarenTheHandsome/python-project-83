from urllib.parse import urlparse


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
