# -*- coding: utf-8 -*-
from collections import defaultdict
from datetime import datetime

from beertools import read_pol_beers, BreweryNameMatcher, BeerNameMatcher

from db import Database


def find_in_list(dicts, key, value):
    return (item for item in dicts if item[key] == value).next()


def findall_in_list(dicts, key, value):
    return [item for item in dicts if item[key] == value]


def get_breweries_polet(beers_polet):
    breweries = list(set([product['Produsent'] for product in beers_polet]))
    return sorted(breweries)


def save_pol_beers(beers, db):
    now = datetime.now()
    for beer in beers:
        beer['created'] = now

    sql = '''
        INSERT INTO pol_beer (id, name, store_category, produktutvalg, producer, distributor, varenummer, abv, volume, color, smell, taste, method, cork_type, packaging_type, price, country, district, subdistrict, url, vintage, ingredients, pairs_with_1, pairs_with_2, pairs_with_3, storage_notes, sweetness, freshness, bitterness, richness, ratebeer_id, created)
        VALUES (%(Varenummer)s, %(Varenavn)s, %(Butikkategori)s, %(Produktutvalg)s, %(Produsent)s, %(Distributor)s, %(Varenummer)s, %(Alkohol)s, %(Volum)s, %(Farge)s, %(Lukt)s, %(Smak)s, %(Metode)s, %(Korktype)s, %(Emballasjetype)s, %(Pris)s, %(Land)s, %(Distrikt)s, %(Underdistrikt)s, %(Vareurl)s, %(Argang)s, %(Rastoff)s, %(Passertil01)s, %(Passertil02)s, %(Passertil03)s, %(Lagringsgrad)s, %(Sodme)s, %(Friskhet)s, %(Bitterhet)s, %(Fylde)s, %(ratebeer_id)s, %(created)s)
        ON CONFLICT (id) DO UPDATE
        SET (id, name, store_category, produktutvalg, producer, distributor, varenummer, abv, volume, color, smell, taste, method, cork_type, packaging_type, price, country, district, subdistrict, url, vintage, ingredients, pairs_with_1, pairs_with_2, pairs_with_3, storage_notes, sweetness, freshness, bitterness, richness, ratebeer_id) = 
        (%(Varenummer)s, %(Varenavn)s, %(Butikkategori)s, %(Produktutvalg)s, %(Produsent)s, %(Distributor)s, %(Varenummer)s, %(Alkohol)s, %(Volum)s, %(Farge)s, %(Lukt)s, %(Smak)s, %(Metode)s, %(Korktype)s, %(Emballasjetype)s, %(Pris)s, %(Land)s, %(Distrikt)s, %(Underdistrikt)s, %(Vareurl)s, %(Argang)s, %(Rastoff)s, %(Passertil01)s, %(Passertil02)s, %(Passertil03)s, %(Lagringsgrad)s, %(Sodme)s, %(Friskhet)s, %(Bitterhet)s, %(Fylde)s, %(ratebeer_id)s);
    '''
    db.run_upserts(sql, beers)


def match_pol_breweries(breweries_pol, breweries_rb):
    grouped = defaultdict(list)

    brewery_matcher = BreweryNameMatcher(breweries_rb)
    for brewery_pol in breweries_pol:
        match = brewery_matcher.match_name(unicode(brewery_pol))
        if match is not None:
            grouped[match['id']].append(brewery_pol)
    return grouped


def match_pol_beer(pol_beer, beer_matcher, db):

    from_db = db.get_pol_brewery(pol_beer['Varenummer'])
    if from_db is not None:
        pol_beer['ratebeer_id'] = from_db['ratebeer_id']
        return pol_beer

    pol_beer_name = pol_beer['Varenavn']
    abv = pol_beer['Alkohol']
    beer_match = beer_matcher.match_name(pol_beer_name, abv=abv)
    ratebeer_id = None
    if beer_match is not None:
        ratebeer_id = beer_match['id']
    pol_beer['ratebeer_id'] = ratebeer_id
    return pol_beer


def match_pol_beers(rb_brewery, rb_beers_for_brewery, pol_breweries, beers_polet, db):
    beer_matcher = BeerNameMatcher(
        rb_brewery,
        rb_beers_for_brewery,
        skip_retired=True
    )
    matched_beers = []
    for pol_brewery in pol_breweries:
        pol_beers = findall_in_list(beers_polet, 'Produsent', pol_brewery)
        for pol_beer in pol_beers:
            matched_beers.append(match_pol_beer(pol_beer, beer_matcher, db))
    return matched_beers


def update_pol_beers(conn_str=None):
    db = Database(conn_str)
    beers_polet, updated = read_pol_beers()

    breweries_rb = db.get_rb_breweries()
    breweries_pol = get_breweries_polet(beers_polet)

    matched_pol_rb = match_pol_breweries(breweries_pol, breweries_rb)

    matched_beers = []
    for rb_beer_id, pol_breweries in matched_pol_rb.iteritems():
        rb_brewery = find_in_list(breweries_rb, 'id', rb_beer_id)['name']
        rb_beers_for_brewery = db.get_rb_beers_for_brewery(rb_beer_id)
        matched_beers += match_pol_beers(
            rb_brewery,
            rb_beers_for_brewery,
            pol_breweries,
            beers_polet,
            db
        )
    save_pol_beers(matched_beers, db)
    db.add_log('pol_beers', updated)

if __name__ == '__main__':
    update_pol_beers()
