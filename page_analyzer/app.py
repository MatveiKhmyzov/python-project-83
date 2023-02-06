import requests
import os
from dotenv import load_dotenv
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    get_flashed_messages,
)
from datetime import datetime
from page_analyzer.validator import (
    check_validity,
    get_check_url,
    get_normalized_url
)
from page_analyzer.data_base import (
    add_url_record,
    add_check_record,
    get_url_by_name,
    get_all_url_records,
    get_url_by_id,
    get_checks_url_by_id,
    get_last_check_url
)


app = Flask(__name__)
load_dotenv()
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.get('/')
def index():
    return render_template('index.html')


@app.post('/urls')
def add_url():
    url_fields_dct = request.form.to_dict()
    url_fields_dct['created_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    normalize_url = get_normalized_url(url_fields_dct['url'])
    errors = check_validity(normalize_url)
    url_fields_dct['url'] = normalize_url
    if errors:
        if errors['name'] == 'Страница уже существует':
            url_record = get_url_by_name(normalize_url)
            id = url_record['id']
            flash(errors['name'], 'alert-primary')
            return redirect(url_for('get_one_url', id=id))
        else:
            flash(errors['name'], 'alert-danger')
            if 'name1' in errors.keys():
                flash(errors["name1"], 'alert-danger')
            errors = get_flashed_messages(with_categories=True)
            return render_template(
                'index.html',
                url=url_fields_dct['url'],
                errors=errors
            ), 422
    else:
        add_url_record(url_fields_dct)
        flash('Страница успешно добавлена', 'alert-success')
        url_record = get_url_by_name(normalize_url)
        id = url_record['id']
        return redirect(url_for('get_one_url', id=id))


@app.get('/urls')
def get_all_urls():
    all_urls = get_all_url_records()
    last_check = get_last_check_url()
    return render_template('urls.html', urls=all_urls, last_check=last_check)


@app.get('/urls/<id>')
def get_one_url(id):
    url = get_url_by_id(id)
    checks = get_checks_url_by_id(id)
    messages = get_flashed_messages(with_categories=True)
    return render_template('url.html',
                           url=url,
                           messages=messages, checks=checks
                           )


@app.post('/urls/<id>/checks')
def add_check(id):
    url_record = get_url_by_id(id)
    url = url_record['name']
    try:
        check_record = get_check_url(id, url)
        if check_record['status_code'] == 200:
            add_check_record(check_record)
            flash('Страница успешно проверена', 'alert-success')
        else:
            flash('Произошла ошибка при проверке', 'alert-danger')
    except requests.RequestException:
        flash('Произошла ошибка при проверке', 'alert-danger')
    return redirect(url_for('get_one_url', id=id))
