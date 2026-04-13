from urllib.parse import urlparse
def validator(url):
    errors = {}
    if len(url) == 0:
        errors['url'] = 'Url не должен быть пустым'
    if len(url) > 255:
        errors['url'] = 'Url не должен быть длиннее 255 символов'

    return errors
    
    # 
    # try:
    #     result = urlparse(url)
    #     # Проверяем наличие схемы (http/https) и домена (netloc)
    #     return all([result.scheme, result.netloc])
    # except ValueError:
    #     return False