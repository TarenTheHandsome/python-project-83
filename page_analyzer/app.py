import requests

import datetime
from urllib.parse import urlparse
from dotenv import load_dotenv
load_dotenv()
from page_analyzer.html_parser import HtmlParser
from page_analyzer.url_validator import validator, name_validator, normalize_url
from page_analyzer.database import (
    add_data_into_urls,
    get_url,
    add_data_in_url_check,
    get_all_urls,
    get_string_by_id,
    get_string_by_url_id
)



from flask import (
    Flask,
    flash,
    get_flashed_messages,
    make_response,
    redirect,
    render_template,
    request,
    url_for,
)


app = Flask(__name__)
app.secret_key = "super secret key"


def get_status_code(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException:
        flash('Произошла ошибка при проверке')
        return None
    return response.status_code


@app.route('/')
def hello():
    return render_template('start_page.html')

@app.post('/')
def post_url():
    form_data = request.form.to_dict()
    url = form_data.get('url')
    error = validator(url)
    name_error = name_validator(url)
    if error:
        return render_template('errors/error.html'), 422
    if name_error:
        return render_template('errors/error.html'), 422
    #соединение с ДБ
    add_data_into_urls(normalize_url(url))
    flash('S', 'success')
    resp = make_response(redirect(url_for('get_url_list')))
    return resp

@app.route('/header')
def header():
    return render_template('header.html')

@app.get('/urls')
def get_url_list():
    #добавить сюда статус код
    all_urls = get_all_urls()
    return render_template('urls.html', all_urls=all_urls)

@app.get('/url/<id>')
def get_id(id):
    name = get_url(id)
    status = get_status_code(name)
    all_urls = get_string_by_id(id)
    return render_template('url.html', all_urls=all_urls, status=status)


@app.get('/urls/<id>/checks')
def get_check(id):
    name = get_url(id)
    status = get_status_code(name)
    all_checks = get_string_by_url_id(id)
    all_urls = get_string_by_id(id)
    return render_template('check_button.html', all_checks=all_checks, all_urls=all_urls, id=id, status=status)


@app.post('/urls/<id>/checks')
def post_check(id):
    name = get_url(id)
    status = get_status_code(name)
    parser = HtmlParser(name)
    add_data_in_url_check(id, status, parser.get_h1(), parser.get_title(), parser.get_description())
    return redirect(url_for('get_check', id=id))
