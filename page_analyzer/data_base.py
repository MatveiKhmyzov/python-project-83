import psycopg2
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
    with conn.cursor() as curs:
        curs.execute('SELECT * FROM urls where name = (%s)', [name])
        url_tuple = curs.fetchone()
    conn.close()
    return url_tuple


def get_url_by_id(id):
    conn = psycopg2.connect(DATABASE_URL)
    with conn.cursor() as curs:
        curs.execute('SELECT * FROM urls where id = (%s)', [id])
        url_tuple = curs.fetchone()
    conn.close()
    return url_tuple


def get_all_url_records():
    conn = psycopg2.connect(DATABASE_URL)
    with conn.cursor() as curs:
        curs.execute('SELECT * FROM urls')
        all_urls_tuple = curs.fetchall()
    conn.close()
    return all_urls_tuple
