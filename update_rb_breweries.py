# -*- coding: utf-8 -*-
import psycopg2
from beertools import read_ratebeer_breweries


def get_connection():
    conn_string = "host='localhost' dbname='beer' user='beer' password='beer'"
    return psycopg2.connect(conn_string)


def update_breweries(breweries):
    conn = get_connection()
    cur = conn.cursor()
    counter = 0
    for brewery in breweries:
        sql = '''
            INSERT INTO rb_brewery AS b (id, name, country, subregion, city)
            VALUES (%(id)s, %(name)s, %(country)s, %(subregion)s, %(city)s)
            ON CONFLICT (id) DO UPDATE
            SET (id, name, country, subregion, city) = (%(id)s, %(name)s, %(country)s, %(subregion)s, %(city)s);
        '''
        cur.execute(sql, (brewery))
        counter += 1
        if counter % 1000 == 0:
            print 'commit at %s' % counter
            conn.commit()

    conn.commit()

    cur.close()
    conn.close()


if __name__ == '__main__':
    breweries = read_ratebeer_breweries()
    update_breweries(breweries)
