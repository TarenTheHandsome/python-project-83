import os

import psycopg2
from dotenv import load_dotenv
from psycopg2.extras import RealDictCursor

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')
conn = psycopg2.connect(DATABASE_URL)


# retrieves all records from the 'urls' table
def get_all_urls():
    sql = '''
    SELECT DISTINCT ON (urls.id)
    urls.id,
    urls.name,
    url_checks.created_at,
    url_checks.status_code
    FROM urls
    LEFT JOIN url_checks ON urls.id = url_checks.url_id
    ORDER BY urls.id, url_checks.created_at DESC;
    '''
    with conn.cursor(cursor_factory=RealDictCursor) as curs:
        curs.execute(sql)
        return curs.fetchall()


# retrieves a row by id from the 'urls' table
def find_url_by_id(id):
    sql = '''
    SELECT *
    FROM urls
    WHERE id = %(id)s'''
    with conn.cursor(cursor_factory=RealDictCursor) as curs:
        curs.execute(sql, {'id': id})
        return curs.fetchall()


# retrieves a row by url_id from the 'url_checks' table
def find_checks_by_url_id(url_id):
    sql = '''
    SELECT *
    FROM url_checks
    WHERE url_id = %(url_id)s
    '''
    with conn.cursor(cursor_factory=RealDictCursor) as curs:
        curs.execute(sql, {'url_id': url_id})
        return curs.fetchall()


# retrieves the URL-name by id from the 'urls' table
def get_url(id):
    sql = '''
    SELECT name
    FROM urls
    WHERE id = %(id)s
    '''
    with conn.cursor(cursor_factory=RealDictCursor) as curs:
        curs.execute(sql, {'id': id})
        return curs.fetchone().get('name')


# adds a URL to the 'urls' table
def save_url(url):
    sql = '''
    INSERT INTO urls (name)
    VALUES (%(url)s)
    RETURNING id;
    '''
    with conn.cursor() as curs:
        curs.execute(sql, {'url': url})
        conn.commit()
        return curs.fetchone()[0]


# adds information to the 'url_check' table.
def save_check(url_id, status_code, h1, title, description):
    sql = '''
    INSERT INTO url_checks (
    url_id,
    status_code,
    h1,
    title,
    description
    )
    VALUES (
    %(url_id)s,
    %(status_code)s,
    %(h1)s,
    %(title)s,
    %(description)s
    );
    '''
    with conn.cursor() as curs:
        curs.execute(sql, {
            'url_id': url_id,
            'status_code': status_code,
            'h1': h1,
            'title': title,
            'description': description
        })
    conn.commit()


# retrieves the status_code by url_id from the 'url_checks' table
def get_status_code_db(url_id):
    sql = '''
    SELECT status_code
    FROM url_checks
    WHERE url_id = %(url_id)s
    ORDER BY created_at DESC LIMIT 1;
    '''
    with conn.cursor(cursor_factory=RealDictCursor) as curs:
        curs.execute(sql, {'url_id': url_id})
        return curs.fetchone()
