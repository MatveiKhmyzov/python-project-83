import validators
import requests
from page_analyzer.data_base import get_url_by_name
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from datetime import datetime


def check_validity(url):
    errors = {}
    url_found = get_url_by_name(url)
    if validators.url(url):
        if url_found:
            errors['name'] = 'Страница уже существует'
    else:
        errors['name'] = 'Некорректный URL'
        if not url:
            errors['name1'] = "URL обязателен"
    return errors


def get_normalized_url(url):
    if url:
        parsed_name = urlparse(url)
        normalize_url = "{0}://{1}".format(
            parsed_name.scheme,
            parsed_name.netloc
        )
    else:
        normalize_url = ''
    return normalize_url


def get_http_response(url):
    http_response = requests.get(url)
    http_response.raise_for_status()
    return http_response


def get_check_url(id, http_response):
    html_file = http_response.text
    code = http_response.status_code
    soup = BeautifulSoup(html_file, 'html.parser')
    h1 = soup.find('h1').text.strip() if soup.find('h1') else ''
    title = soup.find('title').text.strip() if soup.find('title') else ''
    description = soup.find(attrs={"name": "description"})['content'].strip()\
        if soup.find(attrs={"name": "description"}) else ''
    check_record = {'url_id': id,
                    'status_code': code,
                    'h1': h1,
                    'title': title,
                    'description': description,
                    'created_at': datetime.now().strftime("%Y-%m-%d")
                    }
    return check_record
