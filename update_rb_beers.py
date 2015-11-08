# -*- coding: utf-8 -*-
import psycopg2
from beertools import read_ratebeer_beers


def get_connection():
    conn_string = "host='localhost' dbname='beer' user='beer' password='beer'"
    return psycopg2.connect(conn_string)


def update_beers(beers):
    conn = get_connection()
    cur = conn.cursor()
    counter = 0
    for beer in beers:
        sql = '''
            INSERT INTO rb_beer AS b (id, name, shortname, alias, retired, style_id, score_overall, score_style, abv, ibu, brewery_id)
            SELECT %(id)s, %(name)s, %(shortname)s, %(alias)s, %(retired)s, %(style_id)s, %(score_overall)s, %(score_style)s, %(abv)s, %(ibu)s, %(brewery_id)s
            WHERE EXISTS (SELECT id FROM rb_brewery WHERE id=%(brewery_id)s)
            ON CONFLICT (id) DO UPDATE
            SET (id, name, shortname, alias, retired, style_id, score_overall, score_style, abv, ibu, brewery_id) = 
            (%(id)s, %(name)s, %(shortname)s, %(alias)s, %(retired)s, %(style_id)s, %(score_overall)s, %(score_style)s, %(abv)s, %(ibu)s, %(brewery_id)s);
        '''
        cur.execute(sql, (beer))
        counter += 1
        if counter % 1000 == 0:
            print 'commit at %s' % counter
            conn.commit()

    conn.commit()
    cur.close()
    conn.close()


if __name__ == '__main__':
    beers = read_ratebeer_beers()
    update_beers(beers)
