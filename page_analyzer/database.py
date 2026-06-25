import requests
import psycopg2
import os
from dotenv import load_dotenv
import datetime
load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')
conn = psycopg2.connect(DATABASE_URL)
from psycopg2.extras import RealDictCursor





class Validator:
    def __init__(self):
        self.tables = {'urls', 'url_checks'}
        self.orders = {'ASC', 'DESC'}
        self.elements = [{'urls': ''}, {'url_checks': ''}]

    def table_validator(self, table):
        if table in self.tables:
            return False
        return True

    def order_validator(self, order):
        if order in self.orders:
            return False
        return True


def validator(table, order):
    v = Validator()
    errors = []
    if not table or v.table_validator(table):
        errors.append(True)
        raise ValueError(f"Invalid table name. Allowed: {v.tables}")

    order = order.upper()
    if v.order_validator(order):
        errors.append(True)
        raise ValueError(f"Invalid table order. Allowed: {v.tables}")
    return errors


#Достает строчку или строчки из обеих таблиц
def get_data(table=None, order='ASC', id=None):
    if validator(table, order):
        raise ValueError(f"Invalid data")
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
    print(sql)
    with conn.cursor(cursor_factory=RealDictCursor) as curs:
        curs.execute(sql, id_dict)

        return curs.fetchall()
    

#Достает позицию из любой таблицы по id/url_id
def get_element(table, element, id):
    if validator(table, id):
        raise ValueError(f"Invalid data")
    sql = f"SELECT name FROM urls WHERE id = %(id)s"
    with conn.cursor(cursor_factory=RealDictCursor) as curs:
        curs.execute(sql, {'id': id})
        name = curs.fetchone().get('name')
    status = requests.get(name)
    return status.status_code

#Добавляет url в таблицу urls
def add_data(url):
    datatime = datetime.date.today()
    sql = f'INSERT INTO urls (name, created_at) VALUES (%(url)s, %(created_at)s);'
    with conn.cursor() as curs:
        curs.execute(sql, {'url': url, 'created_at': datatime})
    conn.commit()

#Добавляет status_code в таблицу url_checks
def add_url_check(url_id, status_code):
    datatime = datetime.date.today()
    sql = f'INSERT INTO url_checks (url_id, status_code, created_at )' \
          f' VALUES (%(url_id)s, %(status_code)s, %(created_at)s);'
    with conn.cursor() as curs:
        curs.execute(sql, {'url_id': url_id, 'status_code': status_code, 'created_at': datatime})
    conn.commit()

