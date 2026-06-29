import os
import requests
import datetime
from urllib.parse import urlparse
import psycopg2
import os
from dotenv import load_dotenv
load_dotenv()
from page_analyzer.url_validator import validator
from page_analyzer.database import add_data_into_urls
from page_analyzer.database import get_url
from page_analyzer.database import add_url_check
from page_analyzer.database import get_all_urls
from page_analyzer.database import get_string_by_id
from page_analyzer.database import get_string_by_url_id


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


@app.route('/')
def hello():
    return render_template('start_page.html')

@app.post('/')
def post_url():
    form_data = request.form.to_dict()
    url = form_data.get('url')
    datatime = datetime.date.today()
    error = validator(url)
    if error:
        return render_template('error.html'), 422
    #соединение с ДБ
    add_data_into_urls(f'{urlparse(url).scheme}://{urlparse(url).hostname}', datatime)
    flash('S', 'success')
    resp = make_response(redirect(url_for('get_url_list')))
    return resp

@app.route('/header')
def header():
    return render_template('header.html')

@app.get('/urls')
def get_url_list():
    all_urls = get_all_urls()
    return render_template('urls.html', all_urls=all_urls)

@app.get('/url/<id>')
def get_id(id):
    all_urls = get_string_by_id(id)
    return render_template('url.html', all_urls=all_urls)

@app.route('/urls/<id>/checks', methods=['GET', 'POST'])
def check(id):
    name = get_url(id)
    try:
        requests.get(name).raise_for_status()
    except:
        flash('Произошла ошибка при проверке')

    status = requests.get(name)
    add_url_check(id, status.status_code)
    all_checks = get_string_by_url_id(id)
    all_urls = get_string_by_id(id)
    return render_template('check_button.html', all_checks=all_checks, all_urls=all_urls)

