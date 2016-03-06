# -*- coding: utf-8 -*-
import urlparse
from datetime import datetime

import psycopg2

psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)


class Database(object):

    def __init__(self, conn_str=None):
        self.conn_str = conn_str

    def get_connection(self):
        if self.conn_str is None:
            conn_str = "host='localhost' dbname='beer' user='beer' password='beer'"
            return psycopg2.connect(conn_str)
        result = urlparse.urlparse(self.conn_str)
        username = result.username
        password = result.password
        database = result.path[1:]
        hostname = result.hostname
        return psycopg2.connect(
            database=database,
            user=username,
            password=password,
            host=hostname
        )

    def execute_sql(self, sql, data=None):
        conn = self.get_connection()
        cur = conn.cursor()
        if data:
            cur.execute(sql, (data,))
        else:
            cur.execute(sql)
        conn.commit()
        cur.close()
        conn.close()

    def run_upserts(self, sql, items):
        conn = self.get_connection()
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

    def get_rb_beers_for_brewery(self, brewery_id):
        conn = self.get_connection()
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

    def get_pol_brewery(self, id):
        conn = self.get_connection()
        cur = conn.cursor()
        cur.execute('SELECT id, ratebeer_id FROM pol_beer where id=%s', (id,))
        res = cur.fetchone()
        cur.close()
        conn.close()
        if res:
            return {'id': res[0], 'ratebeer_id': res[1]}
        return None

    def get_rb_breweries(self):
        conn = self.get_connection()
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

    def get_rb_breweries_for_country(self, country_id):
        conn = self.get_connection()
        cur = conn.cursor()
        cur.execute('SELECT id, name FROM rb_brewery WHERE country=%s', (country_id,))
        breweries = []
        for row in cur.fetchall():
            breweries.append({
                'id': row[0],
                'name': row[1]
            })
        cur.close()
        conn.close()
        return breweries

    def get_pol_beers(self):
        conn = self.get_connection()
        cur = conn.cursor()
        cur.execute('SELECT id, name FROM pol_beer')
        beers = []
        for row in cur.fetchall():
            beers.append({
                'id': row[0],
                'name': row[1]
            })
        cur.close()
        conn.close()
        return beers

    def get_pol_shops(self):
        conn = self.get_connection()
        cur = conn.cursor()
        cur.execute('SELECT id, name FROM pol_shop')
        shops = []
        for row in cur.fetchall():
            shops.append({
                'id': row[0],
                'name': row[1]
            })
        cur.close()
        conn.close()
        return shops

    def add_log(self, operation_type, last_updated=None):
        if last_updated is None:
            last_updated = datetime.now()
        sql = '''
            INSERT INTO update_log (type, datetime, last_updated)
            VALUES (%(operation_type)s, now(), %(last_updated)s)
        '''
        conn = self.get_connection()
        cur = conn.cursor()
        data = {'operation_type': operation_type, 'last_updated': last_updated}
        cur.execute(sql, data)
        conn.commit()
        cur.close()
        conn.close()
