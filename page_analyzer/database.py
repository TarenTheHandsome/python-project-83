import requests
import psycopg2
import os
from dotenv import load_dotenv
import datetime
load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')
conn = psycopg2.connect(DATABASE_URL)
from psycopg2.extras import RealDictCursor


#достает все записи из таблицы urls
def get_all_urls():
    sql = f"SELECT * FROM urls ORDER BY id DESC"
    with conn.cursor(cursor_factory=RealDictCursor) as curs:
        curs.execute(sql)
        return curs.fetchall()


#достает строчку по id из таблицы urls
def get_string_by_id(id):
    sql = f"SELECT * FROM urls WHERE id = %(id)s"
    with conn.cursor(cursor_factory=RealDictCursor) as curs:
        curs.execute(sql, {'id': id})
        return curs.fetchall()


#достает строчку по url_id из таблицы url_checks
def get_string_by_url_id(url_id):
    sql = f"SELECT * FROM url_checks WHERE url_id = %(url_id)s"
    with conn.cursor(cursor_factory=RealDictCursor) as curs:
        curs.execute(sql, {'url_id': url_id})
        return curs.fetchall()


#достает название сайта по id из таблицы urls
def get_url(id):
    sql = f"SELECT name FROM urls WHERE id = %(id)s"
    with conn.cursor(cursor_factory=RealDictCursor) as curs:
        curs.execute(sql, {'id': id})
        return curs.fetchone().get('name')


def add_data_into_urls(url, created_date):
    sql = f'INSERT INTO urls (name, created_at) VALUES (%(url)s, %(created_at)s);'
    with conn.cursor() as curs:
        curs.execute(sql, {'url': url, 'created_at': created_date})
    conn.commit()


def add_url_check(url_id, status_code):
    datatime = datetime.date.today()
    sql = f'INSERT INTO url_checks (url_id, status_code, created_at )' \
          f' VALUES (%(url_id)s, %(status_code)s, %(created_at)s);'
    with conn.cursor() as curs:
        curs.execute(sql, {'url_id': url_id, 'status_code': status_code, 'created_at': datatime})
    conn.commit()




#Добавляет url в таблицу urls
def add_data(url, created_date):
    sql = f'INSERT INTO urls (name, created_at) VALUES (%(url)s, %(created_at)s);'
    with conn.cursor() as curs:
        curs.execute(sql, {'url': url, 'created_at': created_date})
    conn.commit()

#Добавляет status_code в таблицу url_checks



# def get_check(url_id):
#     sql = f"SELECT * FROM url_checks WHERE url_id = %(url_id)s"
#     with conn.cursor(cursor_factory=RealDictCursor) as curs:
#         curs.execute(sql, {'url_id': url_id})
#         return curs.fetchall()


# def select_id(id):
#     sql = 'SELECT * FROM urls WHERE id = %(id)s;'
#     with conn.cursor(cursor_factory=RealDictCursor) as curs:
#         curs.execute(sql, {'id': id})
#         url = curs.fetchone()
#     return url

# def add_url_check(url_id, status_code):
#     datatime = datetime.date.today()
#     sql = f'INSERT INTO url_checks (url_id, status_code, created_at )' \
#           f' VALUES (%(url_id)s, %(status_code)s, %(created_at)s);'
#     with conn.cursor() as curs:
#         curs.execute(sql, {'url_id': url_id, 'status_code': status_code, 'created_at': datatime})
#     conn.commit()

#Достает позицию из любой таблицы по id/url_id
# def get_element(table, element, id):
#     sql = f"SELECT name FROM urls WHERE id = %(id)s"
#     with conn.cursor(cursor_factory=RealDictCursor) as curs:
#         curs.execute(sql, {'id': id})
#         name = curs.fetchone().get('name')
#     status = requests.get(name)
#     return status.status_code