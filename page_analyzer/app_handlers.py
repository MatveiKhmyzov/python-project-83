from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    get_flashed_messages,
)
import os
from datetime import datetime
from page_analyzer.validator import validate
from page_analyzer.data_base import (
    add_url_in_bd,
    get_url_by_name,
    get_all_url_records,
    get_url_by_id
)


app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.get('/')
def index():
    url_fields_dct = {}
    errors = []
    return render_template('index.html',
                           url_fields_dct=url_fields_dct,
                           errors=errors
                           )


@app.post('/urls')
def add_url():
    url_fields_dct = request.form.to_dict()
    url_fields_dct['created_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    errors = validate(url_fields_dct)
    if errors:
        if errors["name"] == 'Страница уже существует':
            url_tuple = get_url_by_name(url_fields_dct['url'])
            id = url_tuple[0]
            flash(errors["name"], 'alert-primary')
            return redirect(url_for('get_one_url', id=id))
        flash(errors["name"], 'alert-danger')
        if 'name1' in errors.keys():
            flash(errors["name1"], 'alert-danger')
        errors = get_flashed_messages(with_categories=True)
        return render_template(
            'index.html',
            url_fields_dct=url_fields_dct,
            errors=errors
        )
    else:
        add_url_in_bd(url_fields_dct)
        flash('Адрес добавлен', 'alert-success')
        id = get_url_by_name(url_fields_dct['url'])[0]
        return redirect(url_for('get_one_url', id=id))


@app.get('/urls')
def get_all_urls():
    all_urls = get_all_url_records()
    return render_template('urls.html', urls=all_urls)


@app.get('/urls/<id>')
def get_one_url(id):
    url = get_url_by_id(id)
    messages = get_flashed_messages(with_categories=True)
    return render_template('url.html', url=url, messages=messages)
