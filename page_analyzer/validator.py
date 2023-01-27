from page_analyzer.data_base import get_all_url_records
import validators
from urllib.parse import urlparse


def validate(site):  # noqa: C901
    errors = {}
    all_orders = get_all_url_records()
    existed_sites = []
    for order in all_orders:
        existed_sites.append(order[1])
    parsed_name = urlparse(site['url'])
    normalize_name = "{0}://{1}".format(
        parsed_name.scheme,
        parsed_name.netloc
    )
    if normalize_name != '://':
        site['url'] = normalize_name
    for elem in existed_sites:
        if elem.startswith(site['url']):
            errors['name'] = 'Страница уже существует'
    if not validators.url(site['url']):
        errors['name'] = 'Некорректный URL'
        if not site['url']:
            errors['name1'] = "URL обязателен"
    return errors
