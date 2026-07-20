import psycopg2
import os
from dotenv import load_dotenv
load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')
conn = psycopg2.connect(DATABASE_URL)
from psycopg2.extras import RealDictCursor


#достает все записи из таблицы urls
def get_all_urls():
    # добавить сюда статус код
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


#Добавляет url в таблицу urls
def add_data_into_urls(url):
    sql = f'INSERT INTO urls (name) VALUES (%(url)s);'
    with conn.cursor() as curs:
        curs.execute(sql, {'url': url})
    conn.commit()



#Добавляет информацию в таблицу url_check
def add_data_in_url_check(url_id, status_code, h1, title, description):
    sql = f'INSERT INTO url_checks (url_id, status_code, h1, title, description)' \
          f' VALUES (%(url_id)s, %(status_code)s, %(h1)s, %(title)s, %(description)s);' 
    with conn.cursor() as curs:
        curs.execute(sql, {
            'url_id': url_id,
            'status_code': status_code,
            'h1': h1,
            'title': title,
            'description': description
        })
    conn.commit()
