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
        where = 'WHERE id = %(id)s'
        id_dict = {'id': id}
    sql = f"SELECT * FROM {table} {where} ORDER BY id {order}"
    with conn.cursor(cursor_factory=RealDictCursor) as curs:
        curs.execute(sql, id_dict)
        if id:
            return curs.fetchone()
        # data = curs.fetchall()

        return curs.fetchall()
    
def get_check(url_id):
    sql = f"SELECT * FROM url_checks WHERE url_id = %(url_id)s"
    with conn.cursor(cursor_factory=RealDictCursor) as curs:
        curs.execute(sql, {'url_id': url_id})
        return curs.fetchall()


print(get_data('url_checks', 'DESC'))
print(get_data('url_checks', 'ASC', 1))
print(get_data('urls', 'ASC', 7))
print(get_check(7))
def add_data(url):
    datatime = datetime.date.today()
    sql = f'INSERT INTO urls (name, created_at) VALUES (%(url)s, %(created_at)s);'
    with conn.cursor() as curs:
        curs.execute(sql, {'url': url, 'created_at': datatime})
    conn.commit()


def del_string():
    sql = "DELETE FROM urls WHERE id = '13';"
    with conn.cursor() as curs:
        curs.execute(sql)
    conn.commit()





# add_data('https://getbootstrap.com/')
# print(get_data())
# del_string()
# print(select_id(7))

def add_data_check(url_id, status_code):
    datatime = datetime.date.today()
    sql = f'INSERT INTO url_checks (url_id, status_code, created_at )' \
          f' VALUES (%(url_id)s, %(status_code)s, %(created_at)s);'
    with conn.cursor() as curs:
        curs.execute(sql, {'url_id': url_id, 'status_code': status_code, 'created_at': datatime})
    conn.commit()





    
# add_data_check(7, 200)
# print(get_data_check())
# print(select_id_check(1))





