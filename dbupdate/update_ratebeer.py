# -*- coding: utf-8 -*-

from beertools import read_ratebeer_beers, read_ratebeer_breweries

from db import run_upserts


def update_rb_breweries(breweries):

    sql = '''
        INSERT INTO rb_brewery AS b (id, name, country, subregion, city)
        VALUES (%(id)s, %(name)s, %(country)s, %(subregion)s, %(city)s)
        ON CONFLICT (id) DO UPDATE
        SET (id, name, country, subregion, city) = (%(id)s, %(name)s, %(country)s, %(subregion)s, %(city)s);
    '''
    run_upserts(sql, breweries)


def update_rb_beers(beers):
    sql = '''
        INSERT INTO rb_beer AS b (id, name, shortname, alias, retired, style_id, score_overall, score_style, abv, ibu, brewery_id)
        SELECT %(id)s, %(name)s, %(shortname)s, %(alias)s, %(retired)s, %(style_id)s, %(score_overall)s, %(score_style)s, %(abv)s, %(ibu)s, %(brewery_id)s
        WHERE EXISTS (SELECT id FROM rb_brewery WHERE id=%(brewery_id)s)
        ON CONFLICT (id) DO UPDATE
        SET (id, name, shortname, alias, retired, style_id, score_overall, score_style, abv, ibu, brewery_id) = 
        (%(id)s, %(name)s, %(shortname)s, %(alias)s, %(retired)s, %(style_id)s, %(score_overall)s, %(score_style)s, %(abv)s, %(ibu)s, %(brewery_id)s);
    '''
    run_upserts(sql, beers)


def update_ratebeer():

    breweries = read_ratebeer_breweries()
    update_rb_breweries(breweries)

    beers = read_ratebeer_beers()
    update_rb_beers(beers)

if __name__ == '__main__':
    update_ratebeer()
