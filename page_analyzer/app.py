import os
# from url_validator import validator
import requests
import datetime
from urllib.parse import urlparse
import psycopg2
import os
from dotenv import load_dotenv
# from database import add_data
load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')
conn = psycopg2.connect(DATABASE_URL)
from psycopg2.extras import RealDictCursor



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

###DATABASE###
class Validator:
    def __init__(self):
        self.tables = {'urls', 'url_checks'}
        self.orders = {'ASC', 'DESC'}

    def table_validator(self, table):
        if table in self.tables:
            return False
        return True

    def order_validator(self, order):
        if order in self.orders:
            return False
        return True

def get_data(table=None, order='ASC', id=None):
    v = Validator()
    if not table or v.table_validator(table):
        raise ValueError(f"Invalid table name. Allowed: {v.tables}")

    order = order.upper()
    if v.order_validator(order):
        raise ValueError(f"Invalid table order. Allowed: {v.tables}")

    where = ''
    id_dict = {}
    if id:
        if table == 'url_checks':
            where = 'WHERE url_id = %(url_id)s'
            id_dict = {'url_id': id}
        elif table == 'urls':
            where = 'WHERE id = %(id)s'
            id_dict = {'id': id}
    sql = f"SELECT * FROM {table} {where} ORDER BY id {order}"
    with conn.cursor(cursor_factory=RealDictCursor) as curs:
        curs.execute(sql, id_dict)

        return curs.fetchall()

def add_data(url, created_date):
    sql = f'INSERT INTO urls (name, created_at) VALUES (%(url)s, %(created_at)s);'
    with conn.cursor() as curs:
        curs.execute(sql, {'url': url, 'created_at': created_date})
    conn.commit()

def get_check(url_id):
    sql = f"SELECT * FROM url_checks WHERE url_id = %(url_id)s"
    with conn.cursor(cursor_factory=RealDictCursor) as curs:
        curs.execute(sql, {'url_id': url_id})
        return curs.fetchall()

def select_id(id):
    sql = 'SELECT * FROM urls WHERE id = %(id)s;'
    with conn.cursor(cursor_factory=RealDictCursor) as curs:
        curs.execute(sql, {'id': id})
        url = curs.fetchone()
    return url

def get_url(id):
    sql = f"SELECT name FROM urls WHERE id = %(id)s"
    with conn.cursor(cursor_factory=RealDictCursor) as curs:
        curs.execute(sql, {'id': id})
        return curs.fetchone().get('name')
    
def add_url_check(url_id, status_code):
    datatime = datetime.date.today()
    sql = f'INSERT INTO url_checks (url_id, status_code, created_at )' \
          f' VALUES (%(url_id)s, %(status_code)s, %(created_at)s);'
    with conn.cursor() as curs:
        curs.execute(sql, {'url_id': url_id, 'status_code': status_code, 'created_at': datatime})
    conn.commit()

###DATADASE###

###VALIDATOR###
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

###VALIDAROR###

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
    add_data(f'{urlparse(url).scheme}://{urlparse(url).hostname}', datatime)
    flash('S', 'success')
    resp = make_response(redirect(url_for('get_url_list')))
    return resp

@app.route('/header')
def header():
    return render_template('header.html')

@app.get('/urls')
def get_url_list():
    all_urls = get_data('urls', 'DESC')
    return render_template('urls.html', all_urls=all_urls)

@app.get('/url/<id>')
def get_id(id):
    all_urls = get_data('urls', 'ASC', id)
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
    all_checks = get_data('url_checks', 'ASC', id)
    all_urls = get_data('urls', 'ASC', id)
    return render_template('check_button.html', all_checks=all_checks, all_urls=all_urls)




