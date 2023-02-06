import validators
import requests
from page_analyzer.data_base import get_all_url_records
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from datetime import datetime


def validate(url):  # noqa: C901
    errors = {}
    all_orders = get_all_url_records()
    existed_sites = []
    for order in all_orders:
        existed_sites.append(order[1])
    normalize_url = get_normalize_url(url)
    if not validators.url(url):
        errors['name'] = 'Некорректный URL'
        if not url:
            errors['name1'] = "URL обязателен"
    else:
        if normalize_url != '://':
            url = normalize_url
        for elem in existed_sites:
            if elem.startswith(url):
                errors['name'] = 'Страница уже существует'
    return errors


def get_normalize_url(url):
    parsed_name = urlparse(url)
    normalize_url = "{0}://{1}".format(
        parsed_name.scheme,
        parsed_name.netloc
    )
    return normalize_url


def get_check_url(id, url):
    r = requests.get(url)
    code = r.status_code
    html_file = r.text
    soup = BeautifulSoup(html_file, 'html.parser')
    if soup.h1:
        h1 = soup.h1.string
    else:
        h1 = ''
    if soup.title:
        title = soup.title.string
    else:
        title = ''
    if soup.find(attrs={"name": "description"}):
        find_description = soup.find(attrs={"name": "description"})
        description = find_description['content']
    else:
        description = ''
    check_record = {'url_id': id,
                    'status_code': code,
                    'h1': h1,
                    'title': title,
                    'description': description,
                    'created_at': datetime.now().strftime("%Y-%m-%d")
                    }
    return check_record
