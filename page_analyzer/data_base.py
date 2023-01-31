import psycopg2
from psycopg2.extras import DictCursor
import os

DATABASE_URL = os.getenv('DATABASE_URL')


def add_url_in_bd(url_fields_dct):
    conn = psycopg2.connect(DATABASE_URL)
    with conn.cursor() as curs:
        curs.execute('INSERT INTO urls (name, created_at) VALUES (%s, %s)',
                     (url_fields_dct['url'], url_fields_dct['created_at']))
    conn.commit()
    conn.close()


def get_url_by_name(name):
    conn = psycopg2.connect(DATABASE_URL)
    with conn.cursor(cursor_factory=DictCursor) as curs:
        curs.execute('SELECT * FROM urls where name = (%s)', [name])
        url_dct = curs.fetchone()
    conn.close()
    return url_dct


def get_url_by_id(id):
    conn = psycopg2.connect(DATABASE_URL)
    with conn.cursor(cursor_factory=DictCursor) as curs:
        curs.execute('SELECT * FROM urls where id = (%s)', [id])
        url_dct = curs.fetchone()
    conn.close()
    return url_dct


def get_all_url_records():
    conn = psycopg2.connect(DATABASE_URL)
    with conn.cursor(cursor_factory=DictCursor) as curs:
        curs.execute('SELECT * FROM urls')
        all_urls_dct = curs.fetchall()
    conn.close()
    return all_urls_dct


def add_check_in_bd(check_record):
    conn = psycopg2.connect(DATABASE_URL)
    with conn.cursor() as curs:
        curs.execute('INSERT INTO url_checks\
                         (url_id,\
                          status_code,\
                          h1, title,\
                          description,\
                          created_at)\
                     VALUES (%s, %s, %s, %s, %s, %s)',
                     (check_record['url_id'],
                      check_record['status_code'],
                      check_record['h1'],
                      check_record['title'],
                      check_record['description'],
                      check_record['created_at']))
    conn.commit()
    conn.close()


def get_checks_url_by_id(id):
    conn = psycopg2.connect(DATABASE_URL)
    with conn.cursor(cursor_factory=DictCursor) as curs:
        curs.execute('SELECT * FROM url_checks where url_id = (%s)', [id])
        url_dct = curs.fetchall()
    conn.close()
    return url_dct


def get_last_check_url():
    conn = psycopg2.connect(DATABASE_URL)
    with conn.cursor(cursor_factory=DictCursor) as curs:
        curs.execute('SELECT\
                          urls.id,\
                          urls.name,\
                          url_checks.status_code,\
                          url_checks.created_at\
                      FROM urls\
                      LEFT JOIN url_checks ON urls.id = url_id\
                      AND url_checks.id = (SELECT MAX(url_checks.id)\
                                           FROM url_checks\
                                           WHERE url_id = urls.id)\
                      ORDER BY url_checks.created_at DESC')
        url_dct = curs.fetchall()
    conn.close()
    return url_dct
