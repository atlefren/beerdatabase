# -*- coding: utf-8 -*-

from beertools import read_ratebeer_beers, read_ratebeer_breweries

from db import Database


def update_rb_breweries(breweries, db):

    sql = '''
        INSERT INTO rb_brewery AS b (id, name, country, subregion, city)
        VALUES (%(id)s, %(name)s, %(country)s, %(subregion)s, %(city)s)
        ON CONFLICT (id) DO UPDATE
        SET (id, name, country, subregion, city) = (%(id)s, %(name)s, %(country)s, %(subregion)s, %(city)s);
    '''
    db.run_upserts(sql, breweries)


def update_rb_beers(beers, db):
    sql = '''
        INSERT INTO rb_beer AS b (id, name, shortname, alias, retired, style_id, score_overall, score_style, abv, ibu, brewery_id)
        SELECT %(id)s, %(name)s, %(shortname)s, %(alias)s, %(retired)s, %(style_id)s, %(score_overall)s, %(score_style)s, %(abv)s, %(ibu)s, %(brewery_id)s
        WHERE EXISTS (SELECT id FROM rb_brewery WHERE id=%(brewery_id)s)
        ON CONFLICT (id) DO UPDATE
        SET (id, name, shortname, alias, retired, style_id, score_overall, score_style, abv, ibu, brewery_id) = 
        (%(id)s, %(name)s, %(shortname)s, %(alias)s, %(retired)s, %(style_id)s, %(score_overall)s, %(score_style)s, %(abv)s, %(ibu)s, %(brewery_id)s);
    '''
    db.run_upserts(sql, beers)


def update_ratebeer(conn_str=None):
    db = Database(conn_str)
    breweries = read_ratebeer_breweries()
    update_rb_breweries(breweries, db)

    beers = read_ratebeer_beers()
    update_rb_beers(beers, db)
    db.add_log('ratebeer')


if __name__ == '__main__':
    update_ratebeer()
