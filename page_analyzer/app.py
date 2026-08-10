
import requests
from dotenv import load_dotenv
from flask import (
    Flask,
    flash,
    make_response,
    redirect,
    render_template,
    request,
    url_for,
)

from page_analyzer.database import (
    find_checks_by_url_id,
    find_url_by_id,
    get_all_urls,
    get_status_code_db,
    get_url,
    save_check,
    save_url,
)
from page_analyzer.html_parser import HtmlParser
from page_analyzer.url_validator import name_validator, normalize_url, validator

load_dotenv()

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


@app.post('/urls')
def post_url():
    form_data = request.form.to_dict()
    url = form_data.get('url')
    error = validator(url)
    name_error = name_validator(url)
    if error:
        return render_template('errors/error.html'), 422
    if name_error:
        return render_template('errors/error.html'), 422
    # соединение с ДБ
    new_id = save_url(normalize_url(url))
    flash('Страница успешно добавлена', 'success')
    resp = make_response(redirect(url_for('get_id', id=new_id)))
    return resp


@app.route('/header')
def header():
    return render_template('header.html')


@app.get('/urls')
def get_url_list():
    # добавить сюда статус код
    all_urls = get_all_urls()
    return render_template('urls.html', all_urls=all_urls)


@app.get('/urls/<id>')
# ОШИБКА
def get_id(id):
    status = get_status_code_db(id)
    all_urls = find_url_by_id(id)
    return render_template('url.html', all_urls=all_urls, status=status)


@app.get('/urls/<id>/checks')
# ОШИБКА
def get_check(id):
    status = get_status_code_db(id)
    all_checks = find_checks_by_url_id(id)
    all_urls = find_url_by_id(id)
    return render_template('check_button.html', all_checks=all_checks,
                           all_urls=all_urls, id=id, status=status)


@app.post('/urls/<id>/checks')
def post_check(id):
    name = get_url(id)
    parser = HtmlParser(name)
    save_check(id, parser.status_code, parser.get_h1(),
               parser.get_title(), parser.get_description())
    return redirect(url_for('get_check', id=id))
