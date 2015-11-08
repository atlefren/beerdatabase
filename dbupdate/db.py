# -*- coding: utf-8 -*-
import psycopg2

psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)


def get_connection():
    conn_string = "host='localhost' dbname='beer' user='beer' password='beer'"
    return psycopg2.connect(conn_string)


def run_upserts(sql, items):
    conn = get_connection()
    cur = conn.cursor()
    counter = 0
    for item in items:
        cur.execute(sql, (item))
        counter += 1
        if counter % 1000 == 0:
            conn.commit()

    conn.commit()

    cur.close()
    conn.close()


def get_rb_beers_for_brewery(brewery_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        'SELECT id, name, retired, abv FROM rb_beer WHERE brewery_id=%s',
        (brewery_id,)
    )
    beers = []
    for row in cur.fetchall():
        beers.append({
            'id': row[0],
            'name': row[1],
            'retired': row[2],
            'abv': row[3]
        })
    cur.close()
    conn.close()
    return beers


def get_rb_breweries():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('SELECT id, name FROM rb_brewery')
    breweries = []
    for row in cur.fetchall():
        breweries.append({
            'id': row[0],
            'name': row[1]
        })
    cur.close()
    conn.close()
    return breweries
